import sounddevice as sd
import queue
import json
import os
import time
from vosk import Model, KaldiRecognizer

# Caminho para a pasta do modelo descompactado
MODEL_PATH = "utils/modelo_linguagem/vosk-model-small-pt-0.3"

# Inicializa o modelo
model = Model(MODEL_PATH)

# Fila para receber os dados de áudio
q = queue.Queue()

# Callback para capturar áudio
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# Configurações de áudio
samplerate = 16000  # Taxa de amostragem
rec = KaldiRecognizer(model, samplerate)

# Inicia a captura de áudio
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("Fale algo... (Ctrl+C para parar)")

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            print("Você disse:", result.get("text"))
