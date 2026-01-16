# Mood scoring logic
# scoring.py
# -------------------
from enum import Enum

class Mood(Enum):
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"


def score_text(text: str) -> float:
    """
    Returns a mood score between -1 and 1
    """
    positive_words = ["happy", "good", "great", "love"]
    negative_words = ["sad", "bad", "angry", "hate"]

    score = 0
    text = text.lower()

    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    return max(-1, min(1, score / 3))


def classify_mood(score: float) -> Mood:
    if score > 0.3:
        return Mood.POSITIVE
    elif score < -0.3:
        return Mood.NEGATIVE
    return Mood.NEUTRAL


# Handles mood scoring and classification logic

WEIGHTS = {
    "Q1": 1.0, "Q2": 1.2, "Q3": -1.1, "Q4": 1.0, "Q5": 1.1,
    "Q6": 0.9, "Q7": 0.8, "Q8": 1.0, "Q9": 1.2, "Q10": 1.1
}

WORD_SCORES = {
    "heavy": -2, "empty": -2, "overwhelming": -2,
    "tense": -1, "off": -1,
    "okay": 0, "fine": 0,
    "steady": 1, "manageable": 1,
    "hopeful": 2, "clear": 2, "light": 2
}

def classify(score: float) -> str:
    """Convert final numeric score into a mood label"""
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
    """Calculate raw, weighted, and final mood scores"""
    raw = sum(responses.values())
    weighted = sum(responses[q] * WEIGHTS[q] for q in responses)
    word_score = WORD_SCORES.get(fill_word.lower(), 0)
    final = weighted + word_score
    return raw, weighted, final, classify(final)
