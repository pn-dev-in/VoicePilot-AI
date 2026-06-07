import json
from pathlib import Path

PROFILE_FILE = Path("user_data/profile.json")
PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_profile() -> dict:
    if not PROFILE_FILE.exists():
        return {"name": None, "location": None, "preferences": {}}
    return json.loads(PROFILE_FILE.read_text(encoding="utf-8"))

def save_profile(profile: dict):
    PROFILE_FILE.write_text(json.dumps(profile, indent=2), encoding="utf-8")

def set_user_info(key: str, value: str):
    profile = load_profile()
    if key in ["name", "location"]:
        profile[key] = value
    else:
        profile["preferences"][key] = value
    save_profile(profile)

def get_user_info(key: str) -> str:
    profile = load_profile()
    if key in profile:
        return profile[key]
    if key in profile.get("preferences", {}):
        return profile["preferences"][key]
    return None

def get_profile_summary() -> str:
    profile = load_profile()
    parts = []
    if profile.get("name"):
        parts.append(f"Name: {profile['name']}")
    if profile.get("location"):
        parts.append(f"Location: {profile['location']}")
    if profile.get("preferences"):
        prefs = ", ".join([f"{k}: {v}" for k, v in profile["preferences"].items()])
        parts.append(f"Preferences: {prefs}")
    if not parts:
        return "No profile information saved yet."
    return ". ".join(parts)