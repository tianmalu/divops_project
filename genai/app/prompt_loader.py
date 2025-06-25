# app/prompt_loader.py
from string import Template
from typing import List, Tuple
from app.models import TarotCard

def load_tarot_template(path: str = "app/tarot_prompt_template.txt") -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_prompt(template_str: str, question: str, 
                  picks: List[Tuple[TarotCard, bool, str, str, List[str]]]
                 ) -> str:
    cards_lines = []
    for card, upright, meaning, pos, position_keywords in picks:
        orient = "Upright" if upright else "Reversed"
        
        card_info = []
        card_info.append(f"- [{pos.capitalize()}] {card.name}")
        
        if card.arcana:
            card_info.append(f"  Arcana: {card.arcana}")
        if card.number:
            card_info.append(f"  Number: {card.number}")
        if card.suit:
            card_info.append(f"  Suit: {card.suit}")
        
        card_info.append(f"  Orientation: {orient}")
        card_info.append(f"  Meaning: {meaning}")
        
        if card.keywords:
            keywords_text = ", ".join(card.keywords)
            card_info.append(f"  Keywords: {keywords_text}")
        
        if card.fortune_telling:
            fortune_text = " | ".join(card.fortune_telling)
            card_info.append(f"  Fortune Telling: {fortune_text}")
        
        if upright and card.meanings_light:
            light_meanings = " | ".join(card.meanings_light)
            card_info.append(f"  Light Meanings: {light_meanings}")
        elif not upright and card.meanings_shadow:
            shadow_meanings = " | ".join(card.meanings_shadow)
            card_info.append(f"  Shadow Meanings: {shadow_meanings}")
        
        if position_keywords:
            card_info.append(f"  Position Keywords: {', '.join(position_keywords)}")
        
        if card.archetype:
            card_info.append(f"  Archetype: {card.archetype}")
        if card.hebrew_alphabet:
            card_info.append(f"  Hebrew Alphabet: {card.hebrew_alphabet}")
        if card.numerology:
            card_info.append(f"  Numerology: {card.numerology}")
        if card.elemental:
            card_info.append(f"  Element: {card.elemental}")
        if card.mythical_spiritual:
            card_info.append(f"  Mythical/Spiritual: {card.mythical_spiritual}")
        
        if card.keywordsMeaning:
            keyword_meanings = []
            for km in card.keywordsMeaning:
                keyword_meanings.append(f"{km.keyword}: {km.meaning}")
            if keyword_meanings:
                card_info.append(f"  Keyword Meanings: {' | '.join(keyword_meanings)}")
        
        card_text = "\n".join(card_info)
        cards_lines.append(card_text)
    
    cards_text = "\n\n".join(cards_lines) 
    
    tpl = Template(template_str)
    return tpl.substitute(question=question, cards=cards_text)
