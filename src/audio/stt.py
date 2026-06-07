import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile as wav
import time

SAMPLE_RATE = 16000
RECORD_SECONDS = 5  # Fixed recording length

_model = None

def load_model():
    global _model
    if _model is None:
        print("🔄 Loading Whisper model...")
        _model = whisper.load_model("base")
    return _model

def listen(timeout=None) -> str:
    """
    Record for a fixed duration (RECORD_SECONDS) and transcribe.
    timeout parameter is ignored in this version but kept for compatibility.
    """
    print("🎤 Listening... (speak now)")
    audio = sd.rec(
        int(RECORD_SECONDS * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype=np.float32
    )
    sd.wait()  # Wait for recording to finish
    audio = np.squeeze(audio)

    # Optional: compute volume for debug
    rms = np.sqrt(np.mean(audio**2))
    print(f"RMS: {rms:.2f}")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        wav.write(f.name, SAMPLE_RATE, audio)
        result = load_model().transcribe(f.name)
        text = result["text"].strip()
        if not text:
            print("⚠️ No speech detected.")
        return text