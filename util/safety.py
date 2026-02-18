import re
from scoring import detect_crisis

class CrisisDetector:
    """Pillar: Care - Evaluates immediate clinical risk."""
    @staticmethod
    def evaluate(text: str, q9_score: int = 0):
        # 1. PHQ-9 Item 9 Hard-Trigger (Ideation)
        if q9_score > 0:
            return "🔴 CRITICAL", "### ALERT: Positive Suicidal Ideation marker (Item 9)."

        # 2. Linguistic Pattern Match
        if detect_crisis(text):
            return "🔴 CRITICAL", "### ALERT: High-risk linguistic patterns detected."
        
        return "🟢 STABLE", "Standard monitoring protocol active."
