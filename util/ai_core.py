import re

def AnalyzeSentiment(text):
    """
    Pillar: Response
    Analyzes language for signs of hopelessness or psychological distress.
    """
    # Simple heuristic for demonstration; would be replaced by a transformer model
    indicators = ["hopeless", "pointless", "never get better", "tired of fighting"]
    count = sum(1 for word in indicators if word in text.lower())
    
    if count > 2:
        return "High Negative Sentiment / Hopelessness Detected"
    return "Neutral or Stable Sentiment"
