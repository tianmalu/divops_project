from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.rag_engine import call_gemini_api, store_feedback, build_tarot_prompt
from app.models import AskRequest, Feedback, TarotCard, KeywordMeaning
from app.card_engine import layout_three_card

import os
from dotenv import load_dotenv

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
from weaviate.classes.config import Property, DataType, ReferenceProperty


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

WEAVIATE_URL     = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")

if not GEMINI_API_KEY :
    raise RuntimeError("Missing GEMINI_API_KEY in environment")

client = weaviate.connect_to_weaviate_cloud(
    cluster_url = WEAVIATE_URL ,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    skip_init_checks=True,
)

print("Weaviate is ready:", client.is_ready())

def fetch_full_deck() -> List[TarotCard]:
    """Fetch all tarot cards from Weaviate"""
    try:
        tarot_col = client.collections.get("TarotCard")
        
        # Use the correct API method
        all_objs = tarot_col.query.fetch_objects(limit=78)  # 78 cards in a tarot deck
        
        cards = []
        for obj in all_objs.objects:
            # Map your schema properties to TarotCard model
            card_data = {
                "name": obj.properties.get("name", ""),
                "arcana": obj.properties.get("arcana", ""),
                "img": obj.properties.get("img", ""),
                "meanings_light": obj.properties.get("meanings_light", []),
                "meanings_shadow": obj.properties.get("meanings_shadow", []),
                "keywords": obj.properties.get("keywords", []),
                "fortune_telling": obj.properties.get("fortune_telling", []),
            }
            cards.append(TarotCard(**card_data))
        
        return cards
    except Exception as e:
        print(f"Error fetching deck: {e}")
        return []

def generate_daily_reading(user_id: Optional[str] = None) -> dict:
    """
    Generate a daily reading - standalone function for external import.
    This function can be imported by other modules.
    """
    try:
        deck = fetch_full_deck()
        if not deck:
            raise Exception("Failed to fetch tarot deck")
            
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
        
        question = "What guidance do I need for today?"
        prompt = build_tarot_prompt(question, picks)
        answer = call_gemini_api(prompt)
        
        if user_id:
            store_feedback(user_id, picks, answer)

        return {
            "reading_type": "daily_three_card",
            "question": question,
            "cards": cards_for_display,
            "answer": answer,
            "user_id": user_id
        }
    except Exception as e:
        raise Exception(f"Failed to generate daily reading: {str(e)}")

# ── Main FastAPI Application ────────────────────────────────────────────────────
app = FastAPI()

# ── Scenario 0 (Test Case): Simple Question ────────────────────────────────────────────────
@app.get("/predict")
def predict(question: str = Query(...)):
    result = call_gemini_api(question)
    return {"result": result}

# ── Scenario 1: Casual Daily Use ────────────────────────────────────────────────
@app.get("/daily-reading")
def daily_reading(
    user_id: Optional[str] = Query(None, description="Optional user identifier for tracking")
):
    """
    Draws a random 3-card spread for the day and returns a tarot narrative.
    User ID (if provided) will be recorded for analytics or history tracking.
    """
    try:
        result = generate_daily_reading(user_id)
        return result
    except Exception as e:
        print(f"Error in daily_reading endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate daily reading")

# ── Scenario 2: Emotional Decision (custom question + spread) ─────────────────
@app.post("/ask")
async def ask(req: AskRequest):
    deck = fetch_full_deck()
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
    return {"cards": cards_for_display, "answer": answer}


# ── Scenario 3: Data-Driven Learning (feedback) ─────────────────────────────────

@app.post("/feedback")
def submit_feedback(fb: Feedback):
    """
    Store the user's feedback (text +/or rating) in your RAG store.
    """
    store_feedback(fb.dict())
    return {"status": "ok"}