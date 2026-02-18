 from typing import List, Tuple, Dict

# G.R.A.C.E. CLINICAL STANDARDS
# These map raw numeric scores to clinical interventions
SEVERITY_MAPPING = {
    "SEVERE": (20, 27),
    "MODERATELY_SEVERE": (15, 19),
    "MODERATE": (10, 14),
    "MILD": (5, 9),
    "MINIMAL": (0, 4)
}

def get_clinical_tier(numeric_score: float) -> str:
    """Classifies final numeric scores into validated PHQ-9 mood labels."""
    abs_score = abs(numeric_score)
    for label, (low, high) in SEVERITY_MAPPING.items():
        if low <= abs_score <= high:
            return label
    return "MINIMAL" if abs_score < 5 else "CRITICAL"

def score_entry(responses: Dict[str, int], fill_word: str) -> Tuple[float, float, float, str]:
    """
    Pillar: Response
    Refines raw PHQ-9 inputs with fill_word sentiment analysis.
    """
    # 1. Base PHQ-9 Score (0-27)
    raw_score = sum(responses.values())
    
    # 2. Sentiment Adjustment (Your Logic)
    # If the fill_word contains heavy negative sentiment, we apply a 'Weighted Penalty'
    sentiment_penalty = 0.0
    negative_indicators = ["void", "empty", "dark", "done", "heavy"]
    if any(word in fill_word.lower() for word in negative_indicators):
        sentiment_penalty = 3.0  # Significant clinical weight
        
    final_score = raw_score + sentiment_penalty
    mood_class = get_clinical_tier(final_score)
    
    return float(raw_score), sentiment_penalty, final_score, mood_class
