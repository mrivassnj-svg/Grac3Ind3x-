# FastAPI app
# main.py
# -------------------
# FastAPI app for Grac3Ind3x

import os
from datetime import datetime
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models import MoodEntry
from scoring import score_entry
from database import get_session
from orm import MoodEntryORM

ENV = os.getenv("ENV", "dev")  # Set ENV=prod in production

app = FastAPI(
    title="Grac3Ind3x",
    docs_url=None if ENV == "prod" else "/docs",
    redoc_url=None if ENV == "prod" else "/redoc",
)

@app.post("/mood", response_model=MoodEntry)
async def submit_mood(
    user_id: str,
    responses: dict,
    fill_word: str,
    db: AsyncSession = Depends(get_session)
):
    """Receive mood responses, calculate scores, and store in DB"""

    # Score the mood
    raw, weighted, final, mood_class = score_entry(responses, fill_word)

    # Create ORM object for DB
    entry = MoodEntryORM(
        user_id=user_id,
        timestamp=datetime.utcnow(),
        q1=responses.get("Q1"),
        q2=responses.get("Q2"),
        q3=responses.get("Q3"),
        q4=responses.get("Q4"),
        q5=responses.get("Q5"),
        q6=responses.get("Q6"),
        q7=responses.get("Q7"),
        q8=responses.get("Q8"),
        q9=responses.get("Q9"),
        q10=responses.get("Q10"),
        fill_word=fill_word,
        raw_score=raw,
        weighted_score=weighted,
        final_score=final,
        mood_class=mood_class,
    )

    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    # Return API response
    return MoodEntry(
        user_id=entry.user_id,
        timestamp=entry.timestamp,
        responses=responses,
        fill_word=entry.fill_word,
        raw_score=entry.raw_score,
        weighted_score=entry.weighted_score,
        final_score=entry.final_score,
        mood_class=entry.mood_class,
    )
