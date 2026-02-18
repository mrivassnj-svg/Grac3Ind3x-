import re
import random

class AdaptiveRefinementEngine:
    """
    Pillar: Adaptive
    Simulates ML personalization by tracking which coping strategies 
    yield the most 'engagement' and refining the Care Engine's output.
    """
    def __init__(self):
        # Initial success rates for different coping styles
        self.strategy_performance = {
            "grounding": 0.5,
            "distraction": 0.3,
            "social_outreach": 0.4
        }

    def refine_strategy(self, strategy_used, user_responded_positively):
        """
        Adjusts the weights of the engine based on user response.
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
