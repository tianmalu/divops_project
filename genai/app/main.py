# Standard library imports
import os
from typing import List, Optional

# Third-party imports
from dotenv import load_dotenv

# Local imports
from app.rag_engine import call_gemini_api, build_tarot_prompt
from app.models import TarotCard
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

def fetch_full_deck() -> List[TarotCard]:
    """Fetch all tarot cards from Weaviate"""
    logger.info("Fetching full tarot deck from Weaviate")
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
        
        logger.info(f"Successfully fetched {len(cards)} tarot cards")
        return cards
    except Exception as e:
        logger.error(f"Error fetching deck: {e}")
        return []

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

        return {
            "reading_type": "daily_three_card",
            "question": question,
            "cards": cards_for_display,
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
        prompt = build_tarot_prompt(question, picks)
        answer = call_gemini_api(prompt)
        
        return {
            "question": question,
            "cards": cards_for_display,
            "answer": answer,
            "user_id": user_id
        }
    except Exception as e:
        raise Exception(f"Failed to generate ask reading: {str(e)}")