import re
from scoring import detect_crisis # Importing your logic

class CrisisDetector:
    @staticmethod
    def evaluate(text: str, q9_score: int = 0):
        """
        Pillar: Care
        Returns: (Risk Level, Safety Message)
        """
        # 1. Check for PHQ-9 Item 9 (Suicidal Ideation) Hard-Trigger
        if q9_score > 0:
            return "🔴 CRITICAL", "### ALERT: Item 9 (Ideation) Positive. Initiate Safety Protocol."

        # 2. Check for linguistic red flags
        if detect_crisis(text):
            return "🔴 CRITICAL", "### ALERT: Linguistic Red Flags Detected. Urgent Outreach Advised."
        
        return "🟢 STABLE", "Monitoring continues."
