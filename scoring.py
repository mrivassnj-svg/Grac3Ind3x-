from typing import List, Tuple

# Constants for medical flagging (Pillar: Response)
CRISIS_KEYWORDS = ["end", "goodbye", "hurt", "die", "kill", "suicide", "pointless", "better off dead"]

def detect_crisis(text: str) -> bool:
    """Scans for immediate red flags in the fill_word or narrative commentary."""
    if not text:
        return False
    return any(word in text.lower() for word in CRISIS_KEYWORDS)

def calculate_velocity(current_score: float, historical_scores: List[float]) -> float:
    """
    Pillar: Adaptive
    Calculates the 'Velocity of Decline'. 
    A positive delta indicates worsening symptoms in PHQ-9 (0-27 scale).
    """
    if not historical_scores:
        return 0.0
    
    # We compare against the average of the last 3 entries for stability
    recent_history = historical_scores[-3:]
    avg_historical = sum(recent_history) / len(recent_history)
    
    return current_score - avg_historical

def get_clinical_verdict(score: float, velocity: float, crisis_flag: bool) -> Tuple[str, str]:
    """
    Pillar: Care
    Determines escalation level based on score severity and rate of change.
    Note: PHQ-9 Scores 20+ are Severe.
    """
    # 1. Immediate Red Flag (Ideation or Extreme Severity)
    if crisis_flag or score >= 20 or velocity >= 7:
        return "CRITICAL_RED", "Immediate Crisis Intervention Protocol Triggered"
    
    # 2. Significant Deterioration
    if score >= 15 or velocity >= 4:
        return "YELLOW_ALERT", "Significant Clinical Decline: Schedule Urgent Review"
    
    # 3. Stable / Mild
    return "STABLE_GREEN", "Routine Monitoring: No Acute Risk Detected"
