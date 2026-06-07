import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import get_groq_api_key
from groq import Groq

client = Groq(api_key=get_groq_api_key())

TASK_PROMPT = """Decide if the user wants to perform an action. Possible actions:
- save_note: save a note
- read_notes: read saved notes
- play_music: play a song (user says 'play', 'open youtube', 'play song')
- stop_music: stop currently playing music

Respond in JSON ONLY.
Format: {"tool": "save_note|read_notes|play_music|stop_music", "content": "text if needed"}
If the user asks to play any song, tool = "play_music", content = the song name.
If the user asks to stop music, tool = "stop_music", content = "".
"""

def parse_task(user_text: str) -> dict:
    try:
        resp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "system", "content": TASK_PROMPT}, {"role": "user", "content": user_text}],
            temperature=0
        )
        return json.loads(resp.choices[0].message.content.strip())
    except:
        return {"tool": "none", "content": ""}