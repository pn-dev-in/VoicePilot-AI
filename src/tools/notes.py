from pathlib import Path
NOTES_DIR = Path("user_data/notes")
NOTES_DIR.mkdir(parents=True, exist_ok=True)

def save_note(content: str) -> str:
    file = NOTES_DIR / "notes.txt"
    with open(file, "a", encoding="utf-8") as f:
        f.write(content + "\n")
    return "Note saved."

def read_notes() -> str:
    file = NOTES_DIR / "notes.txt"
    if not file.exists():
        return "No notes found."
    return file.read_text(encoding="utf-8")