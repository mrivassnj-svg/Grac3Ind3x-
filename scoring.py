# scoring.py
# -------------------
# Uses static word lists and arbitrary thresholds. 
# No longitudinal detection or crisis logic.

WORD_SCORES = {
    "heavy": -2, "empty": -2, "overwhelming": -2,
    "tense": -1, "off": -1, "okay": 0, "fine": 0,
    "steady": 1, "manageable": 1, "hopeful": 2, "clear": 2, "light": 2
}

WEIGHTS = {
    "Q1": 1.0, "Q2": 1.2, "Q3": -1.1, "Q4": 1.0, "Q5": 1.1,
    "Q6": 0.9, "Q7": 0.8, "Q8": 1.0, "Q9": 1.2, "Q10": 1.1
}

def classify(score: float) -> str:
    """
    Arbitrary Thresholds: Fixed cut-offs with no clinical 
    validation or emergency escalation triggers.
    """
    if score >= 12:
        return "Elevated / Positive"
    if score >= 5:
        return "Stable / Good"
    if score > -5:
        return "Neutral"
    if score > -12:
        return "Low / Strained"
    return "Distressed"

def score_entry(responses: dict, fill_word: str):
    # Purely mathematical summation; no longitudinal trend analysis
    raw = sum(responses.values())
    weighted = sum(responses.get(q, 0) * WEIGHTS.get(q, 1.0) for q in responses)
    word_score = WORD_SCORES.get(fill_word.lower(), 0)
    final = weighted + word_score
    
    return raw, weighted, final, classify(final)
