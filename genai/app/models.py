from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime
import uuid

class KeywordMeaning(BaseModel):
    keyword: str
    meaning: str
    feedback: Optional[List[str]] = Field(default_factory=list)
    source: str
    orientation: str
    position: int

class CardLayout(BaseModel):
    name: str               
    position: str            
    upright: bool            
    meaning: str             
    position_keywords: List[str]  

class TarotCard(BaseModel):
    id: Optional[str] = None
    name: str
    arcana: Optional[str] = None
    number: Optional[str] = None
    suit: Optional[str] = None
    img: Optional[str] = None         
    fortune_telling: List[str] = Field(default_factory=list)
    keywords:          List[str] = Field(default_factory=list)
    meanings_light:    List[str] = Field(default_factory=list)
    meanings_shadow:   List[str] = Field(default_factory=list)
    archetype:         Optional[str] = None
    hebrew_alphabet:   Optional[str] = None
    numerology:        Optional[str] = None
    elemental:         Optional[str] = None
    mythical_spiritual:Optional[str] = None
    questions_to_ask:  List[str] = Field(default_factory=list)
    keywordsMeaning: Optional[List[KeywordMeaning]] = Field(default_factory=list)

class Discussion(BaseModel):
    discussion_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str  # Changed from Optional[str] to str (required)
    created_at: datetime = Field(default_factory=datetime.now)
    topic: Optional[str] = None
    initial_question: str
    initial_response: str
    cards_drawn: List[CardLayout] = Field(default_factory=list)  
    
class FollowupQuestion(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    discussion_id: str
    question: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.now)
    cards_drawn: Optional[List[TarotCard]] = Field(default_factory=list)

class AskRequest(BaseModel):
    question: str
    spread: Optional[str] = "three"    
    user_id: Optional[str] = None 
    discussion_id: Optional[str] = None  

class FollowupRequest(BaseModel):
    discussion_id: str
    question: str
    user_id: Optional[str] = None

class Feedback(BaseModel):
    user_id: str
    question: str
    spread: List[CardLayout]
    model_response: str
    feedback_text: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1 to 5, where 4-5 triggers KeywordMeaning update")
    discussion_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    def model_dump(self, **kwargs):
        """Override model_dump to handle datetime serialization."""
        data = super().model_dump(**kwargs)
        if isinstance(data.get('timestamp'), datetime):
            data['timestamp'] = data['timestamp'].isoformat()
        return data  