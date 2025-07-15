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
    ReadingType, SpreadType
)
from app.rag_engine import call_gemini_api, build_tarot_prompt
from app.card_engine import layout_three_card

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.post("/ask")
async def custom_reading(req: ReadingRequest):
    """Custom tarot reading with full question_id and discussion_id support."""
    try:
        logger.info(f"Custom reading request: {req.question[:50] if req.question else 'No question'}...")
        
        deck = fetch_full_deck()
        if not deck:
            raise HTTPException(status_code=500, detail="Failed to fetch tarot deck")
            
        picks = layout_three_card(deck)
        cards_for_display = [
            {
                "name": card.name,
                "arcana": card.arcana,
                "image_url": card.img,
                "upright": upright,
                "position": position,
                "position_keywords": position_keywords,
                "meaning": meaning,
            }
            for card, upright, meaning, position, position_keywords in picks
        ]
        
        prompt = build_tarot_prompt(req.question or "What guidance do I need?", picks)
        answer = call_gemini_api(prompt)
        
        # Create structured response using the schema
        response = ReadingResponse(
            cards=cards_for_display,
            interpretation=answer,
            question=req.question,
            spread_type=req.spread_type,
            user_id=req.user_id,
            question_id=req.question_id,
            discussion_id=req.discussion_id,
            reading_type=req.reading_type
        )
        
        logger.info(f"Successfully processed custom reading request")
        return response
        
    except ImportError as e:
        logger.error(f"Cannot import required modules: {e}")
        raise HTTPException(status_code=500, detail="Business logic module not available")
    except Exception as e:
        logger.error(f"Custom reading failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process custom reading")

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
    return JSONResponse(
        status_code=422,
        content=error_response.dict()
    )

# Error handler for general HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    error_response = ErrorResponse(
        error=f"http_error_{exc.status_code}",
        message=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)