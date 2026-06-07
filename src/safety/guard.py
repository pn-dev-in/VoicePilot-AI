def safety_decision(intent: str) -> bool:
    if intent in ("QUERY", "TASK"):
        return True
    return False