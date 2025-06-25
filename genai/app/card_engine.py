# reading_engine.py
import random
from typing import List, Tuple
from app.models import TarotCard

POSITION_KEYWORDS = {
    "past":    ["roots", "foundation", "history", "origin"],
    "present": ["focus", "challenge", "opportunity", "awareness"],
    "future":  ["potential", "direction", "outcome", "change"]
}

def draw_cards(deck: List[TarotCard], count: int) -> List[Tuple[TarotCard, bool]]:
    picks = random.sample(deck, count)
    return [(card, random.choice([True, False])) for card in picks]

def interpret_card(card: TarotCard, upright: bool) -> str:
    return card.meanings_light if upright else card.meanings_shadow

def layout_three_card(deck, layout_key="three_past_present_future"):
    drawn = draw_cards(deck, 3)
    positions = ["past", "present", "future"]
    result = []
    for i, (card, upright) in enumerate(drawn):
        pos = positions[i]
        meaning = interpret_card(card, upright)
        position_keywords = POSITION_KEYWORDS[pos]
        result.append((card, upright, meaning, pos, position_keywords))
    return result

def layout_five_card(deck: List[TarotCard]) -> List[Tuple[TarotCard, bool, str]]:
    pass

def layout_celtic_cross(deck: List[TarotCard]) -> List[Tuple[TarotCard, bool, str]]:
    pass
