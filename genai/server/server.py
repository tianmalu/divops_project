# Standard library imports
import json
import logging
import os
import sys
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

# Third-party imports
import uvicorn
import weaviate
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType, ReferenceProperty

# Local imports
from app.main import generate_daily_reading
from app.weaviate_client import get_weaviate_client
from app.logger_config import get_tarot_logger
from server.schemas import (
    ReadingRequest, ReadingResponse, DailyReadingRequest, 
    PredictionRequest, FeedbackRequest, ErrorResponse,
    StartDiscussionRequest, StartDiscussionResponse,
    FollowupQuestionRequest, FollowupQuestionResponse,
)
from app.rag_engine import (
    start_discussion,
    get_discussion, get_discussion_history, 
    call_gemini_api_followup, store_followup_question
)
from app.context_aware_reading import ContextAwareReader, enhance_reading_with_feedback_context
from app.models import Feedback, TarotCard, FollowupQuestion
from app.feedback import process_user_feedback, get_feedback_stats, FeedbackProcessor


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logger
logger = get_tarot_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for FastAPI."""
    # Startup
    try:
        logger.info("Initializing TarotAI server...")
        
        # Initialize Weaviate client and collections
        client = get_weaviate_client()
        initialize_feedback_collections(client)
        
        logger.info("TarotAI server initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize server: {e}")
        raise
    finally:
        if 'client' in locals():
            client.close()
    
    yield
    
    # Shutdown
    logger.info("Shutting down TarotAI server...")

app = FastAPI(
    title="TarotAI GenAI Service", 
    version="1.0.0",
    description="AI-powered tarot reading service with comprehensive reading types",
    lifespan=lifespan
)

@app.get("/genai/health")
async def health_check():
    """Health check endpoint with feedback system status."""
    try:
        # Check Weaviate connection
        client = get_weaviate_client()
        weaviate_status = "healthy"
        
        # Check if feedback collections exist
        feedback_collections = {
            "Feedback": client.collections.exists("Feedback"),
            "KeywordMeaning": client.collections.exists("KeywordMeaning"),
            "ReadingContext": client.collections.exists("ReadingContext")
        }
        
        client.close()
        
        return {
            "status": "healthy", 
            "timestamp": datetime.utcnow(), 
            "version": "1.0.0",
            "service": "TarotAI GenAI",
            "weaviate_status": weaviate_status,
            "feedback_collections": feedback_collections
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow(),
            "version": "1.0.0", 
            "service": "TarotAI GenAI",
            "error": str(e)
        }

@app.get("/genai/daily-reading")
async def daily_reading(
    user_id: Optional[str] = Query(None, description="User ID for tracking daily reading")
):
    """Daily tarot reading - only requires user_id, no question_id or discussion_id."""
    try:
        logger.info(f"Daily reading request for user: {user_id or 'anonymous'}")
        
        # Create daily reading request
        daily_request = DailyReadingRequest(user_id=user_id)
        
        # Generate daily reading using existing function
        result = generate_daily_reading(user_id)
        
        # Ensure the result includes the reading type
        result["reading_type"] = daily_request.reading_type
        
        logger.info(f"Successfully generated daily reading for {user_id or 'anonymous'}")
        return result
        
    except ImportError as e:
        logger.error(f"Cannot import main.py: {e}")
        raise HTTPException(status_code=500, detail="Business logic module not available")
    except Exception as e:
        logger.error(f"Daily reading failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate daily reading")


@app.post("/genai/discussion/start")
async def start_new_discussion(req: StartDiscussionRequest):
    """Start a new discussion with initial question and draw tarot cards."""
    try:
        logger.info(f"Starting new discussion for user {req.user_id}: {req.initial_question}")

        client = get_weaviate_client()
        
        # Start discussion using the imported function
        discussion = start_discussion(
            user_id=req.user_id,
            discussion_id=req.discussion_id,
            initial_question=req.initial_question,
            client=client
        )
        
        # Format cards for response (CardLayout对象)
        cards_for_display = []
        for card in discussion.cards_drawn:
            cards_for_display.append({
                "name": card.name,
                "upright": card.upright,
                "position": card.position,
                "meaning": card.meaning,
                "position_keywords": card.position_keywords
            })
        # Create structured response
        response = StartDiscussionResponse(
            discussion_id=discussion.discussion_id,
            user_id=discussion.user_id,
            initial_question=discussion.initial_question,
            initial_response=discussion.initial_response,
            cards_drawn=cards_for_display,
            created_at=discussion.created_at
        )
        
        logger.info(f"Successfully started discussion: {discussion.discussion_id}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to start discussion: {e}")
        raise HTTPException(status_code=500, detail="Failed to start discussion")
    finally:
        if 'client' in locals():
            client.close()

@app.post("/genai/discussion/{discussion_id}/followup")
async def ask_followup_question(discussion_id: str, req: FollowupQuestionRequest):
    """Ask a followup question in an existing discussion."""
    try:
        logger.info(f"Followup question for discussion {discussion_id}: {req.question[:50]}...")
        
        client = get_weaviate_client()
        
        # Get discussion to retrieve original cards
        discussion = get_discussion(discussion_id, client)
        if not discussion:
            raise HTTPException(status_code=404, detail="Discussion not found")
        
        # Get conversation history
        history = get_discussion_history(discussion_id, client)
        
        # Generate response using original cards
        response = call_gemini_api_followup(
            question=req.question,
            original_cards=discussion.cards_drawn,
            history=history
        )
        
        # Create and store followup question
        followup = FollowupQuestion(
            question_id=str(uuid.uuid4()),
            discussion_id=discussion_id,
            question=req.question,
            response=response,
            timestamp=datetime.now(),
        )
        
        store_followup_question(followup, client)
        
        # Create response
        followup_response = FollowupQuestionResponse(
            question_id=followup.question_id,
            discussion_id=discussion_id,
            question=req.question,
            response=response,
            timestamp=followup.timestamp
        )
        
        logger.info(f"Successfully answered followup question: {followup.question_id}")
        return followup_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to answer followup question: {e}")
        raise HTTPException(status_code=500, detail="Failed to answer followup question")
    finally:
        if 'client' in locals():
            client.close()

@app.post("/genai/discussion/{discussion_id}/feedback")
async def submit_discussion_feedback(discussion_id: str, feedback_data: dict):
    """Submit feedback for a discussion with rating and accuracy assessment."""
    try:
        logger.info(f"Discussion feedback submission for: {discussion_id}")
        
        client = get_weaviate_client()
        
        # Get the discussion to retrieve cards and details
        discussion = get_discussion(discussion_id, client)
        if not discussion:
            raise HTTPException(status_code=404, detail="Discussion not found")
        
        # Create Feedback object
        feedback = Feedback(
            user_id=feedback_data.get("user_id", discussion.user_id),
            question=discussion.initial_question,
            spread=discussion.cards_drawn,
            model_response=discussion.initial_response,
            feedback_text=feedback_data.get("feedback_text"),
            rating=feedback_data.get("rating"),
            discussion_id=discussion_id
        )
        
        # Process the feedback
        result = process_user_feedback(feedback)
        
        logger.info(f"Successfully processed feedback for discussion {discussion_id}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Discussion feedback submission failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit discussion feedback: {str(e)}")
    finally:
        if 'client' in locals():
            client.close()

@app.get("/genai/feedback/stats")
async def get_feedback_statistics(user_id: Optional[str] = Query(None, description="Optional user ID to filter statistics")):
    """Get feedback statistics for analysis."""
    try:
        logger.info(f"Getting feedback statistics for user: {user_id or 'all users'}")
        
        stats = get_feedback_stats(user_id)
        
        logger.info(f"Successfully retrieved feedback statistics")
        return stats
        
    except Exception as e:
        logger.error(f"Failed to get feedback statistics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get feedback statistics: {str(e)}")

@app.get("/genai/feedback/discussion/{discussion_id}")
async def get_discussion_feedback(discussion_id: str):
    """Get feedback for a specific discussion."""
    try:
        logger.info(f"Getting feedback for discussion: {discussion_id}")
        
        client = get_weaviate_client()
        
        # Get feedback from Weaviate
        collection = client.collections.get("Feedback")
        result = collection.query.fetch_objects(
            where=collection.query.Filter.by_property("discussion_id").equal(discussion_id),
            limit=100
        )
        
        feedback_list = []
        for obj in result.objects:
            feedback_list.append({
                "user_id": obj.properties.get("user_id"),
                "rating": obj.properties.get("rating"),
                "feedback_text": obj.properties.get("feedback_text"),
                "timestamp": obj.properties.get("timestamp")
            })
        
        logger.info(f"Found {len(feedback_list)} feedback entries for discussion {discussion_id}")
        return {"discussion_id": discussion_id, "feedback": feedback_list}
        
    except Exception as e:
        logger.error(f"Failed to get discussion feedback: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get discussion feedback: {str(e)}")
    finally:
        if 'client' in locals():
            client.close()

@app.post("/genai/reading/enhanced")
async def get_enhanced_reading(reading_data: dict):
    """Get an enhanced reading that incorporates feedback context."""
    try:
        logger.info("Generating enhanced reading with context")
        
        # Extract data from request
        question = reading_data.get("question", "")
        base_interpretation = reading_data.get("base_interpretation", "")
        cards_data = reading_data.get("cards", [])
        user_id = reading_data.get("user_id")
        
        # Convert cards data to TarotCard objects
        cards = []
        for card_data in cards_data:
            card = TarotCard(
                name=card_data.get("name", ""),
                keywords=card_data.get("keywords", []),
                meanings_light=card_data.get("meanings_light", []),
                meanings_shadow=card_data.get("meanings_shadow", []),
                arcana=card_data.get("arcana"),
                number=card_data.get("number"),
                suit=card_data.get("suit"),
                img=card_data.get("img")
            )
            cards.append(card)
        
        # Get enhanced reading
        enhanced_result = enhance_reading_with_feedback_context(
            question=question,
            cards=cards,
            base_interpretation=base_interpretation
        )
        
        logger.info("Successfully generated enhanced reading")
        return {"enhanced_interpretation": enhanced_result}
        
    except Exception as e:
        logger.error(f"Failed to generate enhanced reading: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate enhanced reading: {str(e)}")
        
def initialize_feedback_collections(client):
    """Initialize Weaviate collections for feedback system."""
    try:
        if not client.collections.exists("Feedback"):
            client.collections.create(
                name="Feedback",
                properties=[
                    Property(name="user_id", data_type=DataType.TEXT),
                    Property(name="question", data_type=DataType.TEXT),
                    Property(name="model_response", data_type=DataType.TEXT),
                    Property(name="feedback_text", data_type=DataType.TEXT),
                    Property(name="rating", data_type=DataType.INT),
                    Property(name="discussion_id", data_type=DataType.TEXT),
                    Property(name="timestamp", data_type=DataType.TEXT),
                    Property(name="cards_drawn", data_type=DataType.TEXT)
                ]
            )
            logger.info("Created Feedback collection")
        
        if not client.collections.exists("KeywordMeaning"):
            client.collections.create(
                name="KeywordMeaning",
                properties=[
                    Property(name="keyword", data_type=DataType.TEXT),
                    Property(name="meaning", data_type=DataType.TEXT),
                    Property(name="feedback", data_type=DataType.TEXT),
                    Property(name="source", data_type=DataType.TEXT),
                    Property(name="orientation", data_type=DataType.TEXT),
                    Property(name="position", data_type=DataType.INT),
                    Property(name="card_name", data_type=DataType.TEXT),
                    Property(name="created_at", data_type=DataType.TEXT),
                    Property(name="updated_at", data_type=DataType.TEXT)
                ]
            )
            logger.info("Created KeywordMeaning collection")
        
        if not client.collections.exists("ReadingContext"):
            client.collections.create(
                name="ReadingContext",
                properties=[
                    Property(name="question", data_type=DataType.TEXT),
                    Property(name="model_response", data_type=DataType.TEXT),
                    Property(name="user_feedback", data_type=DataType.TEXT),
                    Property(name="rating", data_type=DataType.INT),
                    Property(name="user_id", data_type=DataType.TEXT),
                    Property(name="discussion_id", data_type=DataType.TEXT),
                    Property(name="timestamp", data_type=DataType.TEXT),
                    Property(name="spread_info", data_type=DataType.TEXT),
                    Property(name="total_cards", data_type=DataType.INT),
                    Property(name="question_type", data_type=DataType.TEXT),
                    Property(name="source", data_type=DataType.TEXT)
                ]
            )
            logger.info("Created ReadingContext collection")
            
    except Exception as e:
        logger.error(f"Failed to initialize feedback collections: {e}")
        raise

# Error handler for validation errors
@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    error_response = ErrorResponse(
        error="validation_error",
        message="Invalid request data. Please check your input parameters."
    )
    
    # Convert to dict and manually handle datetime serialization
    response_dict = error_response.model_dump()
    if 'timestamp' in response_dict and isinstance(response_dict['timestamp'], datetime):
        response_dict['timestamp'] = response_dict['timestamp'].isoformat()
    
    return JSONResponse(
        status_code=422,
        content=response_dict
    )

# Error handler for general HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    error_response = ErrorResponse(
        error=f"http_error_{exc.status_code}",
        message=exc.detail
    )
    
    # Convert to dict and manually handle datetime serialization
    response_dict = error_response.model_dump()
    if 'timestamp' in response_dict and isinstance(response_dict['timestamp'], datetime):
        response_dict['timestamp'] = response_dict['timestamp'].isoformat()
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_dict
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)