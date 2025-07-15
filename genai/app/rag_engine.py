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
import weaviate
from weaviate.classes.query import Filter, Sort
from datetime import datetime


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

def store_discussion(discussion: Discussion):
    """
    存储新的讨论到Weaviate
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
                "cards_drawn": str([card.dict() for card in discussion.cards_drawn])
            }
        )
        print(f"Stored discussion: {discussion.discussion_id}")
    except Exception as e:
        print(f"Error storing discussion: {e}")

def get_discussion(discussion_id: str) -> Optional[Discussion]:
    """
    根据ID获取讨论
    """
    try:
        if not client.collections.exists("Discussion"):
            return None
            
        discussion_col = client.collections.get("Discussion")
        result = discussion_col.query.fetch_objects(
            where=Filter.by_property("discussion_id").equal(discussion_id),
            limit=1
        )
        
        if result.objects:
            obj = result.objects[0]
            props = obj.properties
            
            # 重新构造 Discussion 对象
            discussion_data = {
                "discussion_id": props.get("discussion_id"),
                "user_id": props.get("user_id"),
                "created_at": datetime.fromisoformat(props.get("created_at")),
                "topic": props.get("topic"),
                "initial_question": props.get("initial_question"),
                "initial_response": props.get("initial_response"),
                "cards_drawn": []  # 暂时为空，因为反序列化复杂
            }
            return Discussion(**discussion_data)
        return None
    except Exception as e:
        print(f"Error getting discussion: {e}")
        return None

def store_followup_question(followup: FollowupQuestion):
    """
    存储后续问题
    """
    try:
        # 检查是否存在 FollowupQuestion 集合，如果不存在则创建
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
                    ),
                    weaviate.classes.config.Property(
                        name="cards_drawn",
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
                "timestamp": followup.timestamp.isoformat(),
                "cards_drawn": str([card.dict() for card in followup.cards_drawn] if followup.cards_drawn else [])
            }
        )
        print(f"Stored followup question: {followup.question_id}")
    except Exception as e:
        print(f"Error storing followup question: {e}")

def get_discussion_history(discussion_id: str) -> List[FollowupQuestion]:
    """
    获取讨论的所有后续问题
    """
    try:
        if not client.collections.exists("FollowupQuestion"):
            return []
            
        followup_col = client.collections.get("FollowupQuestion")
        result = followup_col.query.fetch_objects(
            where=Filter.by_property("discussion_id").equal(discussion_id),
            sort=Sort.by_property("timestamp", ascending=True)
        )
        
        followups = []
        for obj in result.objects:
            props = obj.properties
            followup_data = {
                "question_id": props.get("question_id"),
                "discussion_id": props.get("discussion_id"),
                "question": props.get("question"),
                "response": props.get("response"),
                "timestamp": datetime.fromisoformat(props.get("timestamp")),
                "cards_drawn": []  # 暂时为空
            }
            followups.append(FollowupQuestion(**followup_data))
        
        return followups
    except Exception as e:
        print(f"Error getting discussion history: {e}")
        return []

def build_followup_prompt(question: str, picks, history: List[FollowupQuestion]) -> str:

    context = ""
    if history:
        context = "Previous conversation context:\n"
        for i, h in enumerate(history, 1):
            context += f"Q{i}: {h.question}\nA{i}: {h.response}\n\n"
    
    base_prompt = build_tarot_prompt(question, picks)
    
    if context:
        return f"{context}\nCurrent question and card reading:\n{base_prompt}"
    else:
        return base_prompt

def get_user_discussions_list(user_id: str) -> List[Discussion]:
    try:
        if not client.collections.exists("Discussion"):
            return []
            
        discussion_col = client.collections.get("Discussion")
        result = discussion_col.query.fetch_objects(
            where=Filter.by_property("user_id").equal(user_id),
            sort=Sort.by_property("created_at", ascending=False)
        )
        
        discussions = []
        for obj in result.objects:
            props = obj.properties
            discussion_data = {
                "discussion_id": props.get("discussion_id"),
                "user_id": props.get("user_id"),
                "created_at": datetime.fromisoformat(props.get("created_at")),
                "topic": props.get("topic"),
                "initial_question": props.get("initial_question"),
                "initial_response": props.get("initial_response"),
                "cards_drawn": []  # 暂时为空
            }
            discussions.append(Discussion(**discussion_data))
        
        return discussions
    except Exception as e:
        print(f"Error getting user discussions: {e}")
        return []