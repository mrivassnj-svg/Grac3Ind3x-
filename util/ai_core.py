import random

class AnalyzeSentiment:
    def __init__(self, text):
        self.text = text

    def get_report(self):
        # Integration point for your normalized scoring
        indicators = ["hopeless", "void", "nothing", "tired", "done"]
        score = sum(1 for word in indicators if word in self.text.lower())
        if score > 2:
            return "High Negative Sentiment (Hopelessness Detected)"
        return "Stable Baseline Sentiment"

class AdaptiveRefinementEngine:
    """Pillar: Adaptive - Personalizes resources based on success."""
    def get_best_resource(self):
        # In a full ML version, this queries the DB for 'what worked last time'
        return random.choice(["grounding", "outreach", "breathing"])d on user response.
        In a production environment, this would update a weights file or database.
        """
        learning_rate = 0.1
        if user_responded_positively:
            self.strategy_performance[strategy_used] += learning_rate
        else:
            self.strategy_performance[strategy_used] -= learning_rate
        
        return self.strategy_performance

    def get_best_resource(self):
        # Returns the strategy with the highest success rate for this specific profile
        return max(self.strategy_performance, key=self.strategy_performance.get)

def AnalyzeSentiment(text):
    """
    Pillar: Response
    Analyzes language for signs of hopelessness or psychological distress.
    """
    indicators = ["hopeless", "pointless", "never get better", "tired of fighting", "no way out"]
    score = sum(1 for word in indicators if word in text.lower())
    
    # Simple threshold-based sentiment analysis
    if score >= 2:
        return "High Negative Sentiment: Persistent Hopelessness Detected"
    elif score == 1:
        return "Low Negative Sentiment: Potential Distress Flagged"
    return "Stable Sentiment"
