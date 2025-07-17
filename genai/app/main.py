# Standard library imports
import os
from typing import List, Optional

# Third-party imports
from dotenv import load_dotenv

# Local imports
from app.rag_engine import call_gemini_api, build_tarot_prompt, fetch_full_deck
from app.models import TarotCard, CardLayout
from app.card_engine import layout_three_card
from app.logger_config import get_tarot_logger
from app.weaviate_client import get_weaviate_client

# Setup logger
logger = get_tarot_logger(__name__)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in environment")

client = get_weaviate_client()

print("Weaviate is ready:", client.is_ready())


def generate_daily_reading(user_id: Optional[str] = None) -> dict:
    """
    Generate a daily reading - standalone function for external import.
    This function can be imported by other modules.
    """
    logger.info(f"Generating daily reading for user: {user_id or 'anonymous'}")
    try:
        deck = fetch_full_deck()
        if not deck:
            raise Exception("Failed to fetch tarot deck")
            
        picks = layout_three_card(deck)
        
        question = "What guidance do I need for today?"
        prompt = build_tarot_prompt(question, picks)
        answer = call_gemini_api(prompt)

        return {
            "reading_type": "daily_three_card",
            "question": question,
            "cards": picks,
            "answer": answer,
            "user_id": user_id
        }
    except Exception as e:
        raise Exception(f"Failed to generate daily reading: {str(e)}")

def generate_ask_reading(question: str, user_id: Optional[str] = None) -> dict:
    """
    Generate a reading for a specific question.
    """
    logger.info(f"Generating ask reading for question: {question[:50]}...")
    try:
        deck = fetch_full_deck()
        picks = layout_three_card(deck)
        prompt = build_tarot_prompt(question, picks)
        answer = call_gemini_api(prompt)
        
        return {
            "question": question,
            "cards": picks,
            "answer": answer,
            "user_id": user_id
        }
    except Exception as e:
        raise Exception(f"Failed to generate ask reading: {str(e)}")