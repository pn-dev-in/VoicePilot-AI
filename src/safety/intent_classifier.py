import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_groq_api_key
from groq import Groq

client = Groq(api_key=get_groq_api_key())

INTENT_PROMPT = """Classify the user's intent into one of: QUERY, TASK, SYSTEM_ACTION, REJECT.
Respond ONLY with the category name."""

def classify_intent(user_text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": INTENT_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except:
        return "REJECT"  # safe fallback