import time
import threading
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import get_groq_api_key
from audio.stt import listen
from brain.llm import ask_llm
from voice.tts import speak
from safety.intent_classifier import classify_intent
from safety.guard import safety_decision
from tools.task_parser import parse_task
from tools.executor import execute_tool
from memory.memory_intent import parse_memory_intent
from memory.long_term import remember, recall
from modes.mode_detector import detect_mode
from modes.daily_briefing import run_daily_briefing
from wakeword.openwakeword_detector import WakeWordDetector
from brain.conversation import reset_conversation
from memory.user_profile import set_user_info, get_user_info, get_profile_summary

interaction_lock = threading.Lock()
conversation_active = False

def process_user_input(text):
    print(f"\n📝 You said: {text}")
    
    mode = detect_mode(text)
    if mode == "daily_briefing":
        run_daily_briefing()
        return
    
    mem = parse_memory_intent(text)
    if mem["action"] == "remember":
        remember(mem["key"], mem["value"])
        speak(f"I'll remember that {mem['key']} is {mem['value']}.")
        return
    if mem["action"] == "recall":
        val = recall(mem["key"])
        speak(val)
        return
    
    intent = classify_intent(text)
    print(f"🧭 Intent: {intent}")
    if not safety_decision(intent):
        speak("I can't help with that request.")
        return
    
    if intent == "TASK":
        task = parse_task(text)
        result = execute_tool(task.get("tool", "none"), task.get("content", ""))
        speak(result)
        return
    
    response = ask_llm(text)
    print(f"🤖 Response: {response}")
    if response and response.strip():
        speak(response)
    else:
        speak("I'm not sure how to respond.")
    time.sleep(0.5)  # pause for TTS to finish
    
    lower_text = text.lower()
    if "my name is" in lower_text or "call me" in lower_text:
        import re
        match = re.search(r"(?:my name is|call me) (\w+)", lower_text)
        if match:
            name = match.group(1).capitalize()
            set_user_info("name", name)
            speak(f"Nice to meet you, {name}. I'll remember that.")
            return
    elif "my location is" in lower_text or "i live in" in lower_text:
        match = re.search(r"(?:my location is|i live in) (.+)", lower_text)
        if match:
            location = match.group(1).title()
            set_user_info("location", location)
            speak(f"Got it. You live in {location}.")
            return
    elif "what is my name" in lower_text or "what's my name" in lower_text:
        name = get_user_info("name")
        if name:
            speak(f"Your name is {name}.")
        else:
            speak("I don't know your name yet. Tell me 'my name is X'.")
        return
    elif "tell me about myself" in lower_text or "what do you know about me" in lower_text:
        summary = get_profile_summary()
        speak(summary)
        return

def handle_interaction():
    global conversation_active
    if conversation_active:
        print("⏳ Conversation already active. Say 'bye' to end.")
        return
    if not interaction_lock.acquire(blocking=False):
        print("⏳ Assistant busy.")
        return
    
    conversation_active = True
    try:
        print("\n🎙️ Starting conversation. Say 'bye', 'exit', or 'stop' to end.\n")
        text = listen()
        if not text or len(text.strip()) < 2:
            speak("I didn't catch that. Please try again.")
        else:
            process_user_input(text)
        
        while True:
            print("🎤 Listening for follow-up... (silence timeout 15s)")
            text = listen(timeout=15)
            if not text or len(text.strip()) < 2:
                speak("I didn't hear anything. Are you still there?")
                text = listen(timeout=10)
                if not text or len(text.strip()) < 2:
                    speak("Ending conversation due to silence.")
                    break
            
            if any(phrase in text.lower() for phrase in ["bye", "exit", "stop", "goodbye", "end conversation"]):
                speak("Goodbye! Say my wake word when you need me again.")
                break
            
            process_user_input(text)
    except Exception as e:
        print(f"❌ Conversation error: {e}")
        speak("Sorry, something went wrong. Ending conversation.")
    finally:
        conversation_active = False
        interaction_lock.release()
        print("🔴 Conversation ended.")

def run():
    print("🟢 Assistant ready. Say 'Jarvis' to start a conversation.")
    reset_conversation()
    try:
        import keyboard
        keyboard.add_hotkey('ctrl+shift+space', handle_interaction)
        print("💡 You can also press Ctrl+Shift+Space to start talking.")
    except ImportError:
        pass
    
    detector = WakeWordDetector(handle_interaction, wake_word="jarvis")
    try:
        detector.start()
    except KeyboardInterrupt:
        detector.stop()
        print("🔴 Assistant stopped.")

if __name__ == "__main__":
    run()