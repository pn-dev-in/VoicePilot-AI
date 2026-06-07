import json
from pathlib import Path

MEMORY_FILE = Path("user_data/memory.json")
MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_memory():
    if not MEMORY_FILE.exists():
        return {}
    return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))

def save_memory(memory: dict):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2), encoding="utf-8")

def remember(key: str, value: str):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def recall(key: str) -> str:
    memory = load_memory()
    return memory.get(key, "I don't have that information saved.")