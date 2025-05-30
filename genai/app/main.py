from fastapi import FastAPI, Query
from app.rag_engine import call_gemini_api,call_rag_with_spread,store_feedback
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Optional

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY :
    raise RuntimeError("Missing GEMINI_API_KEY in environment")

app = FastAPI()

@app.get("/predict")
def predict(question: str = Query(...)):
    result = call_gemini_api(question)
    return {"result": result}


# ── Scenario 1: Casual Daily Use ────────────────────────────────────────────────
@app.get("/daily-reading")
def daily_reading(spread_size: int = Query(3, ge=1, le=10)):
    """
    Draws a random 1- or 3-card (or more) spread and returns a tarot narrative.
    """
    # call a helper that draws cards + calls Gemini under the hood:
    result = call_rag_with_spread(question=None, spread_size=spread_size)
    return {"result": result}

# ── Scenario 2: Emotional Decision (custom question + spread) ─────────────────
class Card(BaseModel):
    name: str
    orientation: str  # "upright" or "reversed"

class ReadingRequest(BaseModel):
    question: str
    spread: Optional[List[Card]] = None

@app.post("/reading")
def custom_reading(req: ReadingRequest):
    """
    If the client provides a 'spread', use it; otherwise draw one internally.
    """
    result = call_rag_with_spread(
        question=req.question,
        spread=req.spread
    )
    return {"result": result}


# ── Scenario 3: Data-Driven Learning (feedback) ─────────────────────────────────
class Feedback(BaseModel):
    user_id: str
    question: str
    spread: List[Card]
    model_response: str
    feedback_text: Optional[str] = None
    rating: Optional[int] = None  # e.g. 1–5

@app.post("/feedback")
def submit_feedback(fb: Feedback):
    """
    Store the user’s feedback (text +/or rating) in your RAG store.
    """
    store_feedback(fb.dict())
    return {"status": "ok"}