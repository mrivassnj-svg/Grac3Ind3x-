# Pydantic models
# models.py
# -------------------
# Pydantic schemas for request/response validation

from datetime import datetime
from typing import Dict
from pydantic import BaseModel, Field

class MoodEntry(BaseModel):
    user_id: str
    timestamp: datetime
    responses: Dict[str, int] = Field(..., description="Q1..Q10 mapped to -2..2")
    fill_word: str
    raw_score: int
    weighted_score: float
    final_score: float
    mood_class: str

    class Config:
        orm_mode = True
