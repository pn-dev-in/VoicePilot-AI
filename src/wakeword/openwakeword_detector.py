import sys
import time
import numpy as np
import pyaudio
from openwakeword.model import Model
import openwakeword

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class WakeWordDetector:
    def __init__(self, callback, wake_word="jarvis"):
        self.callback = callback
        self.running = False
        self.wake_word = wake_word.lower()
        self.cooldown = 3          # seconds between triggers
        self.last_trigger_time = 0

        # Download pre-trained models (one-time)
        print("📦 Downloading pre-trained wake word models...")
        openwakeword.utils.download_models()

        # Load the model – it will pick the ONNX version (since tflite missing)
        self.model = Model(wakeword_models=[self.wake_word])
        # Important: openwakeword expects 1280 samples per prediction (80ms at 16kHz)
        self.chunk_size = 1280
        print(f"✅ Loaded model for '{self.wake_word}'. Chunk size: {self.chunk_size}")

        # Setup microphone stream
        self.audio = pyaudio.PyAudio()
        self.stream = None
        try:
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=self.chunk_size
            )
        except Exception as e:
            print(f"❌ Failed to open microphone: {e}")
            sys.exit(1)

        print(f"👂 Listening for '{self.wake_word}'...")

    def start(self):
        self.running = True
        while self.running:
            try:
                # Read exactly one chunk
                audio_bytes = self.stream.read(self.chunk_size, exception_on_overflow=False)
                # Convert bytes to int16 array, then to float32 in range [-1, 1]
                audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)

                prediction = self.model.predict(audio_int16)
                rms = np.sqrt(np.mean(audio_int16.astype(np.float32) ** 2))
                print(
                f"RMS={rms:.2f}",
                f"MIN={audio_int16.min()}",
                f"MAX={audio_int16.max()}"
                )
                score = prediction.get(self.wake_word, 0.0)
                print("Score:", score)   
                if score > 0.002:
                    now = time.time()
                    if int(time.time() * 5) % 5 == 0:  # print every ~5 seconds
                        print(f"Confidence: {score:.3f}")
                    if now - self.last_trigger_time > self.cooldown:
                        print(f"🟢 Wake word '{self.wake_word}' detected! (confidence: {score:.2f})")
                        self.last_trigger_time = now
                        self.callback()
            except Exception as e:
                print(f"⚠️ Error in wake-word loop: {e}")
                # Don't crash – keep listening
                time.sleep(0.1)

    def stop(self):
        self.running = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        print("Stopped wake word detection.")