import pyttsx3
import threading
import time

_lock = threading.Lock()

def speak(text: str):
    """Speak text using pyttsx3 with faster playback rate."""
    if not text or len(text.strip()) == 0:
        return

    with _lock:
        try:
            engine = pyttsx3.init()
            # Increase speech rate (default ~170)
            rate = engine.getProperty('rate')
            engine.setProperty('rate', 170)  # or set absolute: 200
            # Optional: adjust volume
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"TTS error: {e}")
            # Fallback to print if TTS fails
            print(f"Assistant would say: {text}")