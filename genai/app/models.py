from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List

class KeywordMeaning(BaseModel):
    keyword: str
    meaning: str
    feedback: Optional[List[str]] = Field(default_factory=list)
    source: str
    orientation: str
    position: int

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

class AskRequest(BaseModel):
    question: str
    spread: Optional[str] = "three"    
    user_id: Optional[str] = None 

class Feedback(BaseModel):
    user_id: str
    question: str
    spread: List[TarotCard]
    model_response: str
    feedback_text: Optional[str] = None
    rating: Optional[int] = None  # e.g. 1–5