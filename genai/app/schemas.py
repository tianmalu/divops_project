from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid
from datetime import datetime
import re

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
    spread: Optional[List[Card]] = Field(None, description="Custom card spread")
    
    @field_validator('question')
    @classmethod
    def validate_question(cls, v):
        if v and len(v.strip()) == 0:
            raise ValueError('Question cannot be empty')
        return v.strip() if v else v

class ReadingResponse(BaseModel):
    reading_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique reading ID")
    cards: List[Dict[str, Any]] = Field(..., description="Cards in the reading")
    interpretation: str = Field(..., description="AI interpretation of the reading")
    question: Optional[str] = Field(None, description="Original question")
    spread_type: SpreadType = Field(..., description="Type of spread used")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Reading timestamp")

# ═══════════════════════════════════════════════════════════════════════════════
# Feedback Models 
# ═══════════════════════════════════════════════════════════════════════════════

class FeedbackRequest(BaseModel):
    reading_id: str = Field(..., description="ID of the reading")
    user_id: str = Field(..., description="User ID")
    feedback_text: Optional[str] = Field(None, max_length=1000, description="Text feedback")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating from 1-5")
    helpful: Optional[bool] = Field(None, description="Was the reading helpful?")

# ═══════════════════════════════════════════════════════════════════════════════
# Authentication Models 
# ═══════════════════════════════════════════════════════════════════════════════

class UserRegistrationRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=6, max_length=100, description="User password")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username")
    user_type: UserType = Field(UserType.FREE, description="User type")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

class UserLoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(86400, description="Token expiration time in seconds")
    user_info: Dict[str, Any] = Field(..., description="User information")

# ═══════════════════════════════════════════════════════════════════════════════
# Error Models 
# ═══════════════════════════════════════════════════════════════════════════════

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Error timestamp")

# ═══════════════════════════════════════════════════════════════════════════════
# Additional Models
# ═══════════════════════════════════════════════════════════════════════════════

class ReadingHistoryResponse(BaseModel):
    reading_id: str
    question: Optional[str]
    spread_type: SpreadType
    timestamp: datetime
    rating: Optional[int] = None

class StatsResponse(BaseModel):
    total_readings: int = Field(0, description="Total number of readings")
    this_month: int = Field(0, description="Readings this month")
    average_rating: Optional[float] = Field(None, description="Average rating")
    favorite_spread: Optional[SpreadType] = Field(None, description="Most used spread type")

class UserProfile(BaseModel):
    user_id: str
    email: str
    username: Optional[str] = None
    user_type: UserType
    created_at: datetime
    last_login: Optional[datetime] = None
    total_readings: int = 0