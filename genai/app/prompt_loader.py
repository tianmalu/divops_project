from typing import List
from string import Template
from app.models import TarotCard

def load_tarot_template(path: str = "app/tarot_prompt_template.txt") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_prompt(template_str: str, *, question: str, cards: List[tuple]) -> str:
    cards_text = "\n".join(
        f"- [{pos}] {card.name} ({'Upright' if upright else 'Reversed'}): {meaning}"
        for card, upright, meaning, pos in cards
    )
    return Template(template_str).substitute(question=question, cards=cards_text)
