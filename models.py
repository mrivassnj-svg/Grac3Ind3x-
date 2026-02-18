from pydantic import BaseModel, Field, EmailStr, validator
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID, uuid4

class UserAccount(BaseModel):
    """Pillar: Engine - Identity Management"""
    user_uuid: UUID = Field(default_factory=uuid4)
    email: EmailStr
    is_at_risk: bool = False
    last_evaluation: Optional[datetime] = None
    assigned_clinician_id: Optional[str] = None

class MoodEntry(BaseModel):
    """Pillar: Response - Clinical Data Capture"""
    entry_id: UUID = Field(default_factory=uuid4)
    user_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # PHQ-9 Responses: Mapping Q1-Q9 (0-3 scale)
    responses: Dict[str, int]
    fill_word: Optional[str] = None
    
    # Scoring Metadata
    final_score: float = Field(..., ge=-27.0, le=27.0) # Standardized clinical range
    sentiment_magnitude: float = 0.0
    velocity_delta: float = 0.0 # Change from previous session
    
    # Pillar: Care - Immediate Triage
    is_crisis: bool = False
    q9_trigger: bool = False # Specific Suicidal Ideation flag

    @validator('responses')
    def validate_phq9_range(cls, v):
        for q, score in v.items():
            if not 0 <= score <= 3:
                raise ValueError(f"Question {q} score must be between 0 and 3")
        return v

class AlertSystem(BaseModel):
    """Pillar: Care - Notification & Audit Trail"""
    alert_id: UUID = Field(default_factory=uuid4)
    user_id: str
    severity: str = Field(..., pattern="^(YELLOW|RED|CRITICAL)$")
    alert_message: str
    clinician_notified: bool = False
    notification_timestamp: Optional[datetime] = None
    resolution_status: bool = False # Tracking if the alert was cleared by a human

class ClinicalDashboardSummary(BaseModel):
    """Pillar: Guided - View Model for Oversight UI"""
    active_critical_count: int
    high_velocity_drops: List[str] # List of user_ids with rapid decline
    system_load_status: str
