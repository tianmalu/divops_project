from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import json
import random
from google import genai
from google.genai import types

from typing import List, Tuple, Optional
from app.models import TarotCard, Discussion, FollowupQuestion
from app.prompt_loader import load_tarot_template, render_prompt, build_tarot_prompt_smart
from app.card_engine import layout_three_card
import weaviate
from weaviate.classes.query import Filter, Sort
from datetime import datetime
import uuid


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

def check_environment_variables():
    if not API_KEY :
        raise RuntimeError("Missing GEMINI_API_KEY in environment")

def build_tarot_prompt(question: str, picks):
    template_str = load_tarot_template()  
    return render_prompt(template_str, question, picks)

def build_tarot_prompt_with_history(question: str, picks, history: List[dict] = None):
    """
    Build tarot prompt with optional conversation history.
    Uses the smart prompt builder from prompt_loader.
    """
    return build_tarot_prompt_smart(question, picks, history)

def call_gemini_api(prompt: str) -> str:
    """
    Call the Gemini API with the provided prompt and return the response.
    """
    check_environment_variables()
    # Load the configuration from the JSON file
    with open(os.path.join(os.path.dirname(__file__), "gemini_config.json"), "r", encoding="utf-8") as f:
        cfg = json.load(f)

    gen_cfg = types.GenerationConfig(**cfg["generation_config"])
    safe_cfg = [types.SafetySetting(**s) for s in cfg["safety_settings"]]

    gen_cfg = types.GenerateContentConfig(
        **cfg["generation_config"],
        safety_settings=safe_cfg,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    )

    client = genai.Client(api_key = API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=gen_cfg
    )
    # print("Response:", response.text)
    return response.text 

def call_gemini_api_with_history(question: str, picks, history: List[dict] = None) -> str:
    """
    Call the Gemini API with tarot prompt that includes conversation history.
    This is a convenience function that combines prompt building and API calling.
    """
    prompt = build_tarot_prompt_with_history(question, picks, history)
    return call_gemini_api(prompt)

def store_feedback(user_id: str, question: str, feedback: str) -> None:
    # Placeholder for storing feedback
    pass

def store_discussion(discussion: Discussion, client) -> None:
    """
    sture a discussion in Weaviate.
    """
    try:
        if not client.collections.exists("Discussion"):
            client.collections.create(
                name="Discussion",
                properties=[
                    weaviate.classes.config.Property(
                        name="discussion_id",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="user_id",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="created_at",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="topic",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="initial_question",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="initial_response",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="cards_drawn",
                        data_type=weaviate.classes.config.DataType.TEXT
                    )
                ]
            )
        
        discussion_col = client.collections.get("Discussion")
        discussion_col.data.insert(
            properties={
                "discussion_id": discussion.discussion_id,
                "user_id": discussion.user_id,
                "created_at": discussion.created_at.isoformat(),
                "topic": discussion.topic,
                "initial_question": discussion.initial_question,
                "initial_response": discussion.initial_response,
                "cards_drawn": json.dumps([card.model_dump() for card in discussion.cards_drawn])
            }
        )
        print(f"Stored discussion: {discussion.discussion_id}")
    except Exception as e:
        print(f"Error storing discussion: {e}")

def get_discussion(discussion_id: str, client) -> Optional[Discussion]:
    """
    Get a discussion by its ID from Weaviate.
    """
    try:
        if not client.collections.exists("Discussion"):
            return None
            
        discussion_col = client.collections.get("Discussion")
        result = discussion_col.query.fetch_objects(
            limit=100  # Reasonable limit to avoid fetching too many objects
        )
        
        # Filter manually since Weaviate client doesn't support where parameter
        found_discussion = None
        for obj in result.objects:
            if obj.properties.get("discussion_id") == discussion_id:
                found_discussion = obj
                break
        
        if found_discussion:
            obj = found_discussion
            props = obj.properties
            
            cards_drawn = []
            if props.get("cards_drawn"):
                try:
                    import json
                    cards_data = json.loads(props.get("cards_drawn").replace("'", '"'))
                    cards_drawn = [TarotCard(**card_data) for card_data in cards_data]
                except Exception as e:
                    print(f"Error parsing cards_drawn: {e}")
                    # Fallback to eval if json fails
                    try:
                        cards_data = eval(props.get("cards_drawn"))
                        cards_drawn = [TarotCard(**card_data) for card_data in cards_data]
                    except Exception as e2:
                        print(f"Error with eval fallback: {e2}")
                        cards_drawn = []
            
            discussion_data = {
                "discussion_id": props.get("discussion_id"),
                "user_id": props.get("user_id"),
                "created_at": datetime.fromisoformat(props.get("created_at")),
                "topic": props.get("topic"),
                "initial_question": props.get("initial_question"),
                "initial_response": props.get("initial_response"),
                "cards_drawn": cards_drawn
            }
            return Discussion(**discussion_data)
        return None
    except Exception as e:
        print(f"Error getting discussion: {e}")
        return None

def store_followup_question(followup: FollowupQuestion, client) -> None:
    """
    Store a followup question in Weaviate."""
    try:
        if not client.collections.exists("FollowupQuestion"):
            client.collections.create(
                name="FollowupQuestion",
                properties=[
                    weaviate.classes.config.Property(
                        name="question_id",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="discussion_id",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="question",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="response",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="timestamp",
                        data_type=weaviate.classes.config.DataType.TEXT
                    )
                ]
            )
        
        followup_col = client.collections.get("FollowupQuestion")
        followup_col.data.insert(
            properties={
                "question_id": followup.question_id,
                "discussion_id": followup.discussion_id,
                "question": followup.question,
                "response": followup.response,
                "timestamp": followup.timestamp.isoformat()
            }
        )
        print(f"Stored followup question: {followup.question_id}")
    except Exception as e:
        print(f"Error storing followup question: {e}")

def get_discussion_history(discussion_id: str, client) -> List[FollowupQuestion]:
    """
    Get the discussion history for a given discussion ID.
    """
    try:
        if not client.collections.exists("FollowupQuestion"):
            return []
            
        followup_col = client.collections.get("FollowupQuestion")
        result = followup_col.query.fetch_objects(
            limit=100  # Reasonable limit to avoid fetching too many objects
        )
        
        # Filter manually and sort by timestamp
        filtered_followups = []
        for obj in result.objects:
            if obj.properties.get("discussion_id") == discussion_id:
                filtered_followups.append(obj)
        
        # Sort by timestamp
        filtered_followups.sort(key=lambda x: x.properties.get("timestamp", ""))
        
        followups = []
        for obj in filtered_followups:
            props = obj.properties
            followup_data = {
                "question_id": props.get("question_id"),
                "discussion_id": props.get("discussion_id"),
                "question": props.get("question"),
                "response": props.get("response"),
                "timestamp": datetime.fromisoformat(props.get("timestamp")),
                "cards_drawn": []  
            }
            followups.append(FollowupQuestion(**followup_data))
        
        return followups
    except Exception as e:
        print(f"Error getting discussion history: {e}")
        return []

def build_followup_prompt(question: str, original_cards: List[TarotCard], history: List[FollowupQuestion]) -> str:
    """
    Build followup prompt using the original cards from the discussion.
    """
    context = ""
    if history:
        context = "Previous conversation context:\n"
        for i, h in enumerate(history, 1):
            context += f"Q{i}: {h.question}\nA{i}: {h.response}\n\n"
    
    # Convert TarotCard objects to picks format for build_tarot_prompt
    # We need to simulate the picks format: (card, upright, meaning, position, position_keywords)
    picks = []
    positions = ["past", "present", "future"]
    for i, card in enumerate(original_cards[:3]):  # Only take first 3 cards
        position = positions[i] if i < len(positions) else "unknown"
        upright = True  # Default to upright for followup questions
        meaning = card.meanings_light if card.meanings_light else ["No meaning available"]
        position_keywords = ["guidance", "insight", "wisdom"]
        picks.append((card, upright, meaning, position, position_keywords))
    
    base_prompt = build_tarot_prompt(question, picks)
    
    if context:
        return f"{context}\nCurrent question based on the same cards:\n{base_prompt}"
    else:
        return base_prompt

def call_gemini_api_followup(question: str, original_cards: List[TarotCard], history: List[FollowupQuestion] = None) -> str:
    """
    Call the Gemini API for followup questions using original cards from the discussion.
    """
    prompt = build_followup_prompt(question, original_cards, history)
    return call_gemini_api(prompt)

def get_user_discussions_list(user_id: str, client) -> List[Discussion]:
    try:
        if not client.collections.exists("Discussion"):
            return []
            
        discussion_col = client.collections.get("Discussion")
        result = discussion_col.query.fetch_objects(
            limit=1000  # Higher limit for user discussions
        )
        
        # Filter manually and sort by created_at
        filtered_discussions = []
        for obj in result.objects:
            if obj.properties.get("user_id") == user_id:
                filtered_discussions.append(obj)
        
        # Sort by created_at (descending - most recent first)
        filtered_discussions.sort(key=lambda x: x.properties.get("created_at", ""), reverse=True)
        
        discussions = []
        for obj in filtered_discussions:
            props = obj.properties
            
            cards_drawn = []
            if props.get("cards_drawn"):
                try:
                    import json
                    cards_data = json.loads(props.get("cards_drawn").replace("'", '"'))
                    cards_drawn = [TarotCard(**card_data) for card_data in cards_data]
                except Exception as e:
                    print(f"Error parsing cards_drawn: {e}")
                    # Fallback to eval if json fails
                    try:
                        cards_data = eval(props.get("cards_drawn"))
                        cards_drawn = [TarotCard(**card_data) for card_data in cards_data]
                    except Exception as e2:
                        print(f"Error with eval fallback: {e2}")
                        cards_drawn = []
            
            discussion_data = {
                "discussion_id": props.get("discussion_id"),
                "user_id": props.get("user_id"),
                "created_at": datetime.fromisoformat(props.get("created_at")),
                "topic": props.get("topic"),
                "initial_question": props.get("initial_question"),
                "initial_response": props.get("initial_response"),
                "cards_drawn": cards_drawn
            }
            discussions.append(Discussion(**discussion_data))
        
        return discussions
    except Exception as e:
        print(f"Error getting user discussions: {e}")
        return []

def start_discussion(user_id: str, initial_question: str, topic: str, client) -> Discussion:
    """
    Start a new discussion with initial question and draw tarot cards.
    This function creates a new discussion, draws cards, and generates the initial response.
    """
    # Generate unique discussion ID
    discussion_id = str(uuid.uuid4())
    
    # Fetch full deck and draw cards (only once for the entire discussion)
    from app.main import fetch_full_deck  # Import here to avoid circular import
    deck = fetch_full_deck()
    if not deck:
        raise RuntimeError("Failed to fetch tarot deck")
    
    # Draw cards using three-card layout
    picks = layout_three_card(deck)
    
    # Extract TarotCard objects from picks
    cards_drawn = [card for card, upright, meaning, position, position_keywords in picks]
    
    # Generate initial response using the drawn cards
    prompt = build_tarot_prompt(initial_question, picks)
    initial_response = call_gemini_api(prompt)
    
    # Create discussion object
    discussion = Discussion(
        discussion_id=discussion_id,
        user_id=user_id,
        created_at=datetime.now(),
        topic=topic,
        initial_question=initial_question,
        initial_response=initial_response,
        cards_drawn=cards_drawn
    )
    
    # Store discussion in database
    store_discussion(discussion, client)
    
    return discussion