from memory.long_term import load_memory
from voice.tts import speak
from brain.llm import ask_llm

def run_daily_briefing():
    memory = load_memory()
    if not memory:
        speak("You have no saved notes. Tell me something to remember.")
        return
    context = "\n".join([f"- {k}: {v}" for k, v in memory.items()])
    prompt = f"Summarize key points from this user info and suggest one focus: {context}"
    response = ask_llm(prompt)
    speak(response)