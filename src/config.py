from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

def load_env_file():
    """Load environment variables from .env file manually."""
    if not ENV_FILE.exists():
        raise FileNotFoundError(f"No .env file found at {ENV_FILE}")
    
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

load_env_file()  # Load immediately when config is imported

def get_groq_api_key() -> str:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError(f"GROQ_API_KEY not found in {ENV_FILE}")
    return key