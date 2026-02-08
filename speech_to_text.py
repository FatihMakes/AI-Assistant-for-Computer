# vosk_voice.py
import sounddevice as sd
import vosk
import queue
import sys
import json

MODEL_PATH = "C:/Users/90553/Desktop/vosk/vosk-model-small-en-us-0.15" #put your path in here
model = vosk.Model(MODEL_PATH)

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def record_voice(prompt="🎙 I'm listening, sir...", timeout=None, phrase_time_limit=None):

    print(prompt)
    rec = vosk.KaldiRecognizer(model, 16000)

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text.strip():
                    print("👤 You:", text)

                    return text
