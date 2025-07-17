# app/prompt_loader.py
import os
from string import Template
from typing import List, Tuple
from functools import lru_cache
from app.models import TarotCard, CardLayout

@lru_cache(maxsize=2)
def load_tarot_template(path: str = None) -> str:
    """Load tarot prompt template with caching"""
    if path is None:
        # Get the directory of this file and construct the path to the template
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "tarot_prompt_template.txt")
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_card_blocks(picks: List[CardLayout]) -> str:
    """
    Render card information blocks for CardLayout objects.
    """
    cards_lines = []
    for card in picks:
        orient = "Upright" if card.upright else "Reversed"
        card_info = []
        card_info.append(f"- [{card.position.capitalize()}] {card.name}")
        card_info.append(f"  Orientation: {orient}")
        card_info.append(f"  Meaning: {card.meaning}")
        if card.position_keywords:
            card_info.append(f"  Position Keywords: {', '.join(card.position_keywords)}")
        cards_lines.append("\n".join(card_info))
    return "\n\n".join(cards_lines)

def render_prompt(template_str: str, question: str, 
                  picks: List[CardLayout]
                 ) -> str:
    """Render prompt using the basic template"""
    cards_text = render_card_blocks(picks)
    
    tpl = Template(template_str)
    return tpl.safe_substitute(question=question, cards=cards_text)


@lru_cache(maxsize=2)
def load_tarot_with_history_template(path: str = None) -> str:
    """Load template for tarot reading with conversation history (cached)"""
    if path is None:
        # Get the directory of this file and construct the path to the template
        current_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_dir, "tarot_prompt_with_history_template.txt")
    
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_history_context(history: List[dict], max_messages: int = 5) -> str:
    """Render conversation history into readable format"""
    if not history:
        return ""
    
    context_lines = []
    for msg in history[-max_messages:]:
        role = msg.get('role', '')
        content = msg.get('content', '')
        if role == 'user':
            context_lines.append(f"User: {content}")
        elif role == 'assistant':
            context_lines.append(f"Assistant: {content}")
    
    return "\n".join(context_lines)

def render_prompt_with_history(
    template_str: str, 
    question: str, 
    picks: List[CardLayout],
    history_context: str = ""
) -> str:
    """
    Render prompt with conversation history using unified card rendering
    
    Template variables expected:
    - $question: The user's question
    - $tarot_context: Formatted card information
    - $history_context: Previous conversation context
    """
    tarot_context = render_card_blocks(picks)
    
    tpl = Template(template_str)
    return tpl.safe_substitute(
        question=question, 
        tarot_context=tarot_context,
        history_context=history_context
    )

def build_tarot_prompt_smart(
    question: str, 
    picks: List[CardLayout],
    history: List[dict] = None
) -> str:
    """
    Build tarot prompt with optional conversation history
    
    Args:
        question: User's question
        picks: List of (card, upright, meaning, position, position_keywords)
        history: Optional conversation history
    
    Returns:
        Formatted prompt string ready for AI model
    """
    if history and len(history) > 0:
        try:
            template_str = load_tarot_with_history_template()
            history_context = render_history_context(history)
            return render_prompt_with_history(template_str, question, picks, history_context)
        except FileNotFoundError as e:
            print(f"[Warning] Failed to load history template: {e}")
            print(f"[Warning] Falling back to basic template")
            template_str = load_tarot_template()
            return render_prompt(template_str, question, picks)
    else:
        template_str = load_tarot_template()
        return render_prompt(template_str, question, picks)