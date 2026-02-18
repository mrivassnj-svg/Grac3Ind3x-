from fastapi import FastAPI, Depends, BackgroundTasks
from database import get_db
from scoring import score_entry
from utils.safety import CrisisDetector
from models import MoodEntry, TriageVerdict

app = FastAPI(title="G.R.A.C.E. Systems Core API")

@app.post("/process_entry", response_model=TriageVerdict)
async def process_clinical_entry(
    user_id: str, 
    responses: dict, 
    narrative: str, 
    db: AsyncSession = Depends(get_db)
):
    """
    The Unified Central Logic:
    1. Scores the entry.
    2. Runs crisis detection.
    3. Persists to the Clinical Vault.
    4. Returns a clinical verdict.
    """
    raw, weight, final, mood_class = score_entry(responses, narrative)
    risk_level, safety_msg = CrisisDetector.evaluate(narrative, q9_score=responses.get("Q9", 0))
    
    # ... Database logic (ORM save) ...
    
    return {
        "risk_level": risk_level,
        "score": final,
        "mood_label": mood_class,
        "intervention": safety_msg
    }
