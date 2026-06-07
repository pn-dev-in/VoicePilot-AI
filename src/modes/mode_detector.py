def detect_mode(text: str) -> str:
    triggers = ["what should i do today", "daily briefing", "help me plan my day", "what should i focus on"]
    if any(t in text.lower() for t in triggers):
        return "daily_briefing"
    return "normal"