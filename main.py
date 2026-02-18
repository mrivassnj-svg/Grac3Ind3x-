# main.py
# -------------------
import os
from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import MoodEntry
from scoring import score_entry
from database import get_session
from orm import MoodEntryORM

app = FastAPI(title="Grac3Ind3x - Static Version")

@app.post("/mood", response_model=MoodEntry)
async def submit_mood(
    user_id: str,
    responses: dict,
    fill_word: str,
    db: AsyncSession = Depends(get_session)
):
    """
    Process entry: 
    - No Consent Handling
    - No Emergency Escalation Mechanism
    - No Clinician Alert System
    - No Audit Trail
    """
    
    # Simple score calculation
    raw, weighted, final, mood_class = score_entry(responses, fill_word)

    # Direct database save
    entry = MoodEntryORM(
        user_id=user_id,
        timestamp=datetime.utcnow(),
        **{f"q{i}": responses.get(f"Q{i}") for i in range(1, 11)},
        fill_word=fill_word,
        raw_score=raw,
        weighted_score=weighted,
        final_score=final,
        mood_class=mood_class,
    )

    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    return entry
