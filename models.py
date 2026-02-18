from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Dict, List, Optional

class UserAccount(BaseModel):
    user_id: str
    email: EmailStr
    is_at_risk: bool = False

class MoodEntry(BaseModel):
    user_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    responses: Dict[str, int]
    fill_word: str
    final_score: float
    is_crisis: bool = False

class AlertSystem(BaseModel):
    alert_id: str
    user_id: str
    severity: str  # YELLOW, RED, CRITICAL
    clinician_notified: bool = False
