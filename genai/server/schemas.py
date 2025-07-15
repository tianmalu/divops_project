from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid
from datetime import datetime
import re
import json

# Global configuration for datetime serialization
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# ═══════════════════════════════════════════════════════════════════════════════
# Enums 
# ═══════════════════════════════════════════════════════════════════════════════

class CardOrientation(str, Enum):
    UPRIGHT = "upright"
    REVERSED = "reversed"

class SpreadType(str, Enum):
    SINGLE = "single"
    THREE_CARD = "three"
    FIVE_CARD = "five"
    CELTIC_CROSS = "celtic_cross"

class UserType(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    ADMIN = "admin"

class ReadingType(str, Enum):
    DAILY = "daily"
    CUSTOM = "custom"
    PREDICTION = "prediction"

# ═══════════════════════════════════════════════════════════════════════════════
# Card Models 
# ═══════════════════════════════════════════════════════════════════════════════

class Card(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Card name")
    orientation: CardOrientation = Field(..., description="Card orientation")
    position: Optional[str] = Field(None, description="Position in spread")
    meaning: Optional[str] = Field(None, description="Card meaning")

# ═══════════════════════════════════════════════════════════════════════════════
# Reading Models
# ═══════════════════════════════════════════════════════════════════════════════

class ReadingRequest(BaseModel):
    question: Optional[str] = Field(None, max_length=500, description="Question to ask")
    spread_type: SpreadType = Field(SpreadType.THREE_CARD, description="Type of spread")
    user_id: Optional[str] = Field(None, description="User ID")
    question_id: Optional[str] = Field(None, description="Unique question ID")
    discussion_id: Optional[str] = Field(None, description="Discussion thread ID")
    reading_type: ReadingType = Field(ReadingType.CUSTOM, description="Type of reading")
    spread: Optional[List[Card]] = Field(None, description="Custom card spread")
    
    @field_validator('question')
    @classmethod
    def validate_question(cls, v):
        if v and len(v.strip()) == 0:
            raise ValueError('Question cannot be empty')
        return v.strip() if v else v

class DailyReadingRequest(BaseModel):
    """Daily reading only requires user_id, no question_id or discussion_id"""
    user_id: Optional[str] = Field(None, description="User ID for daily reading")
    reading_type: ReadingType = Field(ReadingType.DAILY, description="Type of reading")

class PredictionRequest(BaseModel):
    """Simple prediction request with question only"""
    question: str = Field(..., min_length=1, max_length=500, description="Question to ask")
    user_id: Optional[str] = Field(None, description="User ID")
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique question ID")
    discussion_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Discussion thread ID")
    reading_type: ReadingType = Field(ReadingType.PREDICTION, description="Type of reading")

class ReadingResponse(BaseModel):
    reading_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique reading ID")
    cards: List[Dict[str, Any]] = Field(..., description="Cards in the reading")
    interpretation: str = Field(..., description="AI interpretation of the reading")
    question: Optional[str] = Field(None, description="Original question")
    spread_type: SpreadType = Field(..., description="Type of spread used")
    user_id: Optional[str] = Field(None, description="User ID")
    question_id: Optional[str] = Field(None, description="Question ID")
    discussion_id: Optional[str] = Field(None, description="Discussion thread ID")
    reading_type: ReadingType = Field(..., description="Type of reading")
    is_followup: bool = Field(default=False, description="Whether this is a followup to an existing discussion")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Reading timestamp")

# ═══════════════════════════════════════════════════════════════════════════════
# Discussion Models
# ═══════════════════════════════════════════════════════════════════════════════

class StartDiscussionRequest(BaseModel):
    """Request to start a new discussion with initial question"""
    user_id: str = Field(..., description="User ID")
    initial_question: str = Field(..., min_length=1, max_length=500, description="Initial question to start discussion")
    topic: str = Field(..., min_length=1, max_length=200, description="Discussion topic/title")
    
    @field_validator('initial_question')
    @classmethod
    def validate_initial_question(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Initial question cannot be empty')
        return v.strip()
    
    @field_validator('topic')
    @classmethod
    def validate_topic(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Topic cannot be empty')
        return v.strip()

class StartDiscussionResponse(BaseModel):
    """Response after starting a new discussion"""
    discussion_id: str = Field(..., description="Generated discussion ID")
    user_id: str = Field(..., description="User ID")
    topic: str = Field(..., description="Discussion topic")
    initial_question: str = Field(..., description="Initial question")
    initial_response: str = Field(..., description="AI response to initial question")
    cards_drawn: List[Dict[str, Any]] = Field(..., description="Cards drawn for this discussion")
    created_at: datetime = Field(..., description="Discussion creation timestamp")

class DiscussionMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique message ID")
    discussion_id: str = Field(..., description="Discussion thread ID")
    user_id: str = Field(..., description="User ID")
    message: str = Field(..., max_length=1000, description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Message timestamp")

class DiscussionResponse(BaseModel):
    discussion_id: str = Field(..., description="Discussion thread ID")
    question_id: str = Field(..., description="Related question ID")
    reading_id: Optional[str] = Field(None, description="Related reading ID")
    messages: List[DiscussionMessage] = Field(default_factory=list, description="Discussion messages")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Discussion creation timestamp")

# ═══════════════════════════════════════════════════════════════════════════════
# Feedback Models 
# ═══════════════════════════════════════════════════════════════════════════════

class FeedbackRequest(BaseModel):
    reading_id: str = Field(..., description="ID of the reading")
    user_id: str = Field(..., description="User ID")
    question_id: Optional[str] = Field(None, description="Question ID")
    discussion_id: Optional[str] = Field(None, description="Discussion thread ID")
    feedback_text: Optional[str] = Field(None, max_length=1000, description="Text feedback")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1-5")
    helpful: Optional[bool] = Field(None, description="Was the reading helpful?")

# ═══════════════════════════════════════════════════════════════════════════════
# Error Models 
# ═══════════════════════════════════════════════════════════════════════════════

class ErrorResponse(BaseModel):
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )
    
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")

# ═══════════════════════════════════════════════════════════════════════════════
# Additional Models
# ═══════════════════════════════════════════════════════════════════════════════

class ReadingHistoryResponse(BaseModel):
    reading_id: str
    question: Optional[str]
    question_id: Optional[str]
    discussion_id: Optional[str]
    spread_type: SpreadType
    reading_type: ReadingType
    timestamp: datetime
    rating: Optional[int] = None

class StatsResponse(BaseModel):
    total_readings: int = Field(0, description="Total number of readings")
    this_month: int = Field(0, description="Readings this month")
    average_rating: Optional[float] = Field(None, description="Average rating")
    favorite_spread: Optional[SpreadType] = Field(None, description="Most used spread type")
    daily_readings: int = Field(0, description="Daily readings count")
    custom_readings: int = Field(0, description="Custom readings count")
    prediction_readings: int = Field(0, description="Prediction readings count")

class UserProfile(BaseModel):
    user_id: str
    email: str
    username: Optional[str] = None
    user_type: UserType
    created_at: datetime
    last_login: Optional[datetime] = None
    total_readings: int = 0
    daily_readings: int = 0
    custom_readings: int = 0
    prediction_readings: int = 0

# ═══════════════════════════════════════════════════════════════════════════════
# Question Models
# ═══════════════════════════════════════════════════════════════════════════════

class Question(BaseModel):
    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique question ID")
    user_id: str = Field(..., description="User ID")
    question_text: str = Field(..., max_length=500, description="Question content")
    category: Optional[str] = Field(None, description="Question category")
    tags: Optional[List[str]] = Field(default_factory=list, description="Question tags")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Question creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Question update timestamp")

class QuestionResponse(BaseModel):
    question_id: str
    user_id: str
    question_text: str
    category: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    related_readings: List[str] = Field(default_factory=list, description="Related reading IDs")
    discussion_id: Optional[str] = Field(None, description="Associated discussion ID")
    created_at: datetime
    updated_at: Optional[datetime] = None

class FollowupQuestionRequest(BaseModel):
    """Request to ask a followup question in an existing discussion"""
    question: str = Field(..., min_length=1, max_length=500, description="Followup question")
    user_id: Optional[str] = Field(None, description="User ID (optional for validation)")
    
    @field_validator('question')
    @classmethod
    def validate_question(cls, v):
        if len(v.strip()) == 0:
            raise ValueError('Question cannot be empty')
        return v.strip()

class FollowupQuestionResponse(BaseModel):
    """Response to a followup question"""
    question_id: str = Field(..., description="Generated question ID")
    discussion_id: str = Field(..., description="Discussion ID")
    question: str = Field(..., description="Followup question")
    response: str = Field(..., description="AI response")
    timestamp: datetime = Field(..., description="Question timestamp")