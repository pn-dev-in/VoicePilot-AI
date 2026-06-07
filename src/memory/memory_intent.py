import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_groq_api_key
from groq import Groq

client = Groq(api_key=get_groq_api_key())

PROMPT = """Decide if the user wants to:
- remember: store a personal fact
- recall: retrieve a stored fact
- none

Respond in JSON only.
Format: {"action": "remember|recall|none", "key": "", "value": ""}"""

def parse_memory_intent(user_text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0
        )
        raw = response.choices[0].message.content.strip()
        return json.loads(raw)
    except:
        return {"action": "none", "key": "", "value": ""}