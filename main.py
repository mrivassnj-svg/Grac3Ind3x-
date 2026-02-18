import os
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

# G.R.A.C.E. Systems Imports
from models import MoodEntry
from scoring import score_entry
from database import get_db  # Updated to use our high-performance generator
from orm import MoodEntryORM, AuditLogORM
from utils.safety import CrisisDetector

app = FastAPI(title="G.R.A.C.E. Systems - Production API")

async def trigger_emergency_workflow(user_id: str, final_score: float, alert_msg: str):
    """
    Pillar: Care
    Background task to notify clinicians or emergency services without 
    blocking the user's API response.
    """
    # Logic for SMS/Email/PagerDuty integration goes here
    print(f"CRITICAL ALERT for {user_id}: {alert_msg}")

@app.post("/mood", response_model=MoodEntry)
async def submit_mood(
    user_id: str,
    responses: dict,
    fill_word: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    G.R.A.C.E. Process Entry:
    - Automated Risk Detection (Safety Pillar)
    - Real-time Triage Escalation (Care Pillar)
    - HIPAA-Compliant Audit Logging (Engine Pillar)
    """
    
    # 1. PILLAR: RESPONSE - Clinical Scoring
    raw, weighted, final, mood_class = score_entry(responses, fill_word)

    # 2. PILLAR: CARE - Immediate Crisis Detection
    # Scan responses specifically for PHQ-9 Item 9 triggers
    risk_level, alert_msg = CrisisDetector.evaluate(str(responses) + " " + fill_word)
    
    if risk_level == "🔴 CRITICAL":
        background_tasks.add_task(trigger_emergency_workflow, user_id, final, alert_msg)

    # 3. PILLAR: ENGINE - Persistent Storage
    entry = MoodEntryORM(
        user_id=user_id,
        timestamp=datetime.now(timezone.utc),
        **{f"q{i}": responses.get(f"Q{i}", 0) for i in range(1, 11)},
        fill_word=fill_word,
        raw_score=raw,
        weighted_score=weighted,
        final_score=final,
        mood_class=mood_class,
        is_crisis=(risk_level == "🔴 CRITICAL")
    )

    # 4. PILLAR: AUDIT - Medico-Legal Accountability
    audit = AuditLogORM(
        action=f"MOOD_SUBMISSION_{risk_level}",
        target_id=user_id,
        timestamp=datetime.now(timezone.utc)
    )

    db.add(entry)
    db.add(audit)
    
    try:
        await db.commit()
        await db.refresh(entry)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database Transaction Failed")

    return entry
