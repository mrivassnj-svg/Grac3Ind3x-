# Constants for medical flagging
CRISIS_KEYWORDS = ["end", "goodbye", "hurt", "die", "kill", "suicide", "pointless"]

def detect_crisis(text: str) -> bool:
    """Scans for immediate red flags in the fill_word or commentary."""
    return any(word in text.lower() for word in CRISIS_KEYWORDS)

def calculate_slope(current_score: float, historical_scores: List[float]) -> float:
    """Calculates the 'Major Drop'—the difference between current and avg mood."""
    if not historical_scores:
        return 0.0
    avg = sum(historical_scores) / len(historical_scores)
    return current_score - avg

def get_clinical_verdict(score: float, slope: float, crisis_flag: bool):
    """Determines escalation level based on psychological factors."""
    if crisis_flag or score < -15 or slope < -8:
        return "CRITICAL_RED", "Immediate Professional Intervention Triggered"
    if score < -8 or slope < -4:
        return "YELLOW_ALERT", "Major Mood Shift Detected: Notify Clinician"
    return "STABLE", "Normal Monitoring"
