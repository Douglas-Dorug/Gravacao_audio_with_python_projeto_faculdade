import sounddevice as sd
import queue
import json
import os
import time
from vosk import Model, KaldiRecognizer

# Caminho para o modelo Vosk (ajustado conforme a estrutura do projeto)
MODEL_PATH = "utils/modelo_linguagem/vosk-model-small-pt-0.3"

# Inicializa o modelo
model = Model(MODEL_PATH)

# Comando Reconhecido
Comando_completo = []

# Fila para capturar o áudio em tempo real
q = queue.Queue()

# Callback para inserir os dados capturados na fila
def callback(indata, frames, time_info, status):
    if status:
        print(f"Aviso de áudio: {status}")
    q.put(bytes(indata))

# Parâmetros de áudio
samplerate = 16000  # Vosk espera 16000 Hz
rec = KaldiRecognizer(model, samplerate)

# Duração da gravação
DURACAO_SEGUNDOS = 10

print(f"Gravando por {DURACAO_SEGUNDOS} segundos...")

# Captura do áudio
with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    inicio = time.time()
    while time.time() - inicio < DURACAO_SEGUNDOS:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            texto = result.get("text", "").strip()
            if texto:
                print("Parcial:", texto)
                Comando_completo.append(texto)
                DURACAO_SEGUNDOS += 3 #aumenta a duração enquanto o comando for falado

# Resultado final após os 10 segundos
resultado_final = json.loads(rec.FinalResult())
texto_final = resultado_final.get("text", "").strip()
print("\n🗣️ Texto reconhecido:", Comando_completo or "[Nada foi reconhecido]")
