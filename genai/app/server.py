from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from datetime import datetime
import logging

import uvicorn

from app.main import generate_daily_reading
from app.models import AskRequest
from app.rag_engine import call_gemini_api, build_tarot_prompt
from app.card_engine import layout_three_card

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TarotAI GenAI Service", version="1.0.0")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow(), "version": "1.0.0"}

@app.get("/predict")
async def predict(question: str = Query(...)):
    logger.info(f"Simple prediction request: {question[:50]}...")
    result = f"Thank you for asking: {question}. Here is your guidance: Focus on the present moment and trust your intuition."
    return {"result": result}

@app.get("/daily-reading")
async def daily_reading(user_id: Optional[str] = Query(None)):
    try:
        logger.info(f"Daily reading request for user: {user_id or 'anonymous'}")
        result = generate_daily_reading(user_id)
        logger.info(f"Successfully generated reading for {user_id or 'anonymous'}")
        return result
        
    except ImportError as e:
        logger.error(f"Cannot import main.py: {e}")
        raise HTTPException(status_code=500, detail="Business logic module not available")
    except Exception as e:
        logger.error(f"Daily reading failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate daily reading")

# ── Scenario 2: Emotional Decision (custom question + spread) ─────────────────
@app.post("/ask")
async def ask(req: AskRequest):
    try:
        logger.info(f"Custom ask request: {req.question[:50]}...")
        
        # Import fetch_full_deck from main.py
        from app.main import fetch_full_deck
        
        deck = fetch_full_deck()
        if not deck:
            raise HTTPException(status_code=500, detail="Failed to fetch tarot deck")
            
        picks = layout_three_card(deck)
        cards_for_display = [
            {
                "name":     card.name,
                "arcana":   card.arcana,
                "image_url":card.img,
                "upright":  upright,
                "position": position,
                "position_keywords": position_keywords,
                "meaning": meaning,
            }
            for card, upright, meaning, position, position_keywords in picks
        ]
        
        prompt = build_tarot_prompt(req.question, picks)
        answer = call_gemini_api(prompt)
        
        result = {
            "question": req.question,
            "cards": cards_for_display, 
            "answer": answer,
            "reading_type": "custom_three_card"
        }
        
        logger.info(f"Successfully processed custom ask request")
        return result
        
    except ImportError as e:
        logger.error(f"Cannot import required modules: {e}")
        raise HTTPException(status_code=500, detail="Business logic module not available")
    except Exception as e:
        logger.error(f"Ask request failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process ask request")

# Keep the old GET /ask endpoint for backward compatibility
@app.get("/ask-simple")
async def ask_simple(question: str = Query(...), user_id: Optional[str] = Query(None)):
    try:
        logger.info(f"Simple ask request for user {user_id or 'anonymous'}: {question[:50]}...")
        result = generate_daily_reading(user_id)  # Reusing the daily reading logic
        logger.info(f"Successfully processed simple ask request for {user_id or 'anonymous'}")
        return result
        
    except ImportError as e:
        logger.error(f"Cannot import main.py: {e}")
        raise HTTPException(status_code=500, detail="Business logic module not available")
    except Exception as e:
        logger.error(f"Simple ask request failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to process simple ask request")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)