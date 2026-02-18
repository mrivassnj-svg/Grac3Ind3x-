class CrisisDetector:
    """
    Pillar: Care
    Specific detection for crisis markers and PHQ-9 Item 9 triggers.
    """
    @staticmethod
    def evaluate(text):
        critical_keywords = ["suicide", "end it all", "better off dead", "kill myself"]
        
        # PHQ-9 Item 9 Logic
        for word in critical_keywords:
            if re.search(rf"\b{word}\b", text.lower()):
                return "🔴 CRITICAL", "### ALERT: Tier 1 Crisis Intervention Required."
        
        return "🟢 STABLE", "Monitoring continues."
