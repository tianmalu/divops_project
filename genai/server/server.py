from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import uvicorn

from app.main import generate_daily_reading, fetch_full_deck
from server.schemas import (
    ReadingRequest, ReadingResponse, DailyReadingRequest, 
    PredictionRequest, FeedbackRequest, ErrorResponse,
    StartDiscussionRequest, StartDiscussionResponse,
    FollowupQuestionRequest, FollowupQuestionResponse,
    ReadingType, SpreadType
)
from app.rag_engine import (
    call_gemini_api, build_tarot_prompt, start_discussion,
    get_discussion, get_discussion_history, get_user_discussions_list,
    call_gemini_api_followup, store_followup_question
)
from app.card_engine import layout_three_card
from app.main import fetch_full_deck
from datetime import datetime
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
from weaviate.classes.config import Property, DataType, ReferenceProperty

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_weaviate_client():
    """Initialize and return Weaviate client"""
    WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")
    
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
        skip_init_checks=True,
    )

app = FastAPI(
    title="TarotAI GenAI Service", 
    version="1.0.0",
    description="AI-powered tarot reading service with comprehensive reading types"
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.utcnow(), 
        "version": "1.0.0",
        "service": "TarotAI GenAI"
    }

@app.get("/predict")
async def predict(
    question: str = Query(..., description="Question for prediction"),
    user_id: Optional[str] = Query(None, description="User ID for tracking")
):
    """Simple prediction endpoint with basic guidance."""
    try:
        logger.info(f"Prediction request from user {user_id or 'anonymous'}: {question[:50]}...")
        
        # Create prediction request object
        pred_request = PredictionRequest(
            question=question,
            user_id=user_id
        )
        
        # For simple predictions, we can use direct AI call
        result = call_gemini_api(f"Please provide brief tarot guidance for: {question}")
        
        response = {
            "question": pred_request.question,
            "result": result,
            "question_id": pred_request.question_id,
            "discussion_id": pred_request.discussion_id,
            "user_id": pred_request.user_id,
            "reading_type": pred_request.reading_type,
            "timestamp": datetime.utcnow()
        }
        
        logger.info(f"Successfully generated prediction for user {user_id or 'anonymous'}")
        return response
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate prediction")

@app.get("/daily-reading")
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

@app.get("/discussions/{user_id}")
async def get_user_discussions(user_id: str):
    """Get all discussions for a user."""
    try:
        logger.info(f"Getting discussions for user: {user_id}")
        
        client = get_weaviate_client()
        
        from app.rag_engine import get_user_discussions_list
        discussions = get_user_discussions_list(user_id, client)
        
        # Format discussions for response
        discussions_response = []
        for discussion in discussions:
            discussions_response.append({
                "discussion_id": discussion.discussion_id,
                "topic": discussion.topic,
                "initial_question": discussion.initial_question,
                "initial_response": discussion.initial_response,
                "created_at": discussion.created_at,
                "cards_count": len(discussion.cards_drawn)
            })
        
        logger.info(f"Found {len(discussions)} discussions for user {user_id}")
        return {"discussions": discussions_response}
        
    except Exception as e:
        logger.error(f"Failed to get discussions for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get discussions")
    finally:
        if 'client' in locals():
            client.close()

@app.get("/discussion/{discussion_id}")
async def get_discussion_details(discussion_id: str):
    """Get details of a specific discussion including cards and history."""
    try:
        logger.info(f"Getting discussion details: {discussion_id}")
        
        client = get_weaviate_client()
        
        from app.rag_engine import get_discussion, get_discussion_history
        
        # Get discussion
        discussion = get_discussion(discussion_id, client)
        if not discussion:
            raise HTTPException(status_code=404, detail="Discussion not found")
        
        # Get discussion history
        history = get_discussion_history(discussion_id, client)
        
        # Format cards for response
        cards_for_display = []
        for card in discussion.cards_drawn:
            cards_for_display.append({
                "name": card.name,
                "arcana": card.arcana,
                "image_url": card.img,
                "keywords": card.keywords,
                "meanings_light": card.meanings_light,
                "meanings_shadow": card.meanings_shadow
            })
        
        # Format history
        history_response = []
        for h in history:
            history_response.append({
                "question_id": h.question_id,
                "question": h.question,
                "response": h.response,
                "timestamp": h.timestamp
            })
        
        response = {
            "discussion_id": discussion.discussion_id,
            "user_id": discussion.user_id,
            "topic": discussion.topic,
            "initial_question": discussion.initial_question,
            "initial_response": discussion.initial_response,
            "cards_drawn": cards_for_display,
            "created_at": discussion.created_at,
            "history": history_response
        }
        
        logger.info(f"Successfully retrieved discussion: {discussion_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get discussion {discussion_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get discussion")
    finally:
        if 'client' in locals():
            client.close()

@app.post("/discussion/start")
async def start_new_discussion(req: StartDiscussionRequest):
    """Start a new discussion with initial question and draw tarot cards."""
    try:
        logger.info(f"Starting new discussion for user {req.user_id}: {req.topic}")
        
        client = get_weaviate_client()
        
        # Start discussion using the imported function
        discussion = start_discussion(
            user_id=req.user_id,
            initial_question=req.initial_question,
            topic=req.topic,
            client=client
        )
        
        # Format cards for response
        cards_for_display = []
        for card in discussion.cards_drawn:
            cards_for_display.append({
                "name": card.name,
                "arcana": card.arcana,
                "image_url": card.img,
                "keywords": card.keywords,
                "meanings_light": card.meanings_light,
                "meanings_shadow": card.meanings_shadow
            })
        
        # Create structured response
        response = StartDiscussionResponse(
            discussion_id=discussion.discussion_id,
            user_id=discussion.user_id,
            topic=discussion.topic,
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

@app.post("/discussion/{discussion_id}/followup")
async def ask_followup_question(discussion_id: str, req: FollowupQuestionRequest):
    """Ask a followup question in an existing discussion."""
    try:
        logger.info(f"Followup question for discussion {discussion_id}: {req.question[:50]}...")
        
        client = get_weaviate_client()
        
        from app.rag_engine import get_discussion, get_discussion_history, call_gemini_api_followup, store_followup_question
        from app.models import FollowupQuestion
        import uuid
        
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
            cards_drawn=[]  # Don't store new cards, use original ones
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

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback for a tarot reading."""
    try:
        logger.info(f"Feedback submission for reading: {feedback.reading_id}")
        
        # Here you would implement your feedback storage logic
        # For now, just log the feedback
        logger.info(f"Feedback received - Rating: {feedback.rating}, Helpful: {feedback.helpful}")
        
        return {
            "status": "success",
            "message": "Feedback submitted successfully",
            "reading_id": feedback.reading_id,
            "timestamp": datetime.utcnow()
        }
        
    except Exception as e:
        logger.error(f"Feedback submission failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit feedback")

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