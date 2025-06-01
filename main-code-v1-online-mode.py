import speech_recognition as sr

# Inicializa o reconhecedor
reconhecedor = sr.Recognizer()

# Usa o microfone como fonte de áudio
with sr.Microphone() as fonte:
    print("Fale algo...")
    reconhecedor.adjust_for_ambient_noise(fonte)  # ajusta ruído ambiente
    audio = reconhecedor.listen(fonte)

    try:
        texto = reconhecedor.recognize_google(audio, language='pt-BR')
        print("Você disse: " + texto)
    except sr.UnknownValueError:
        print("Não consegui entender o que foi dito.")
    except sr.RequestError:
        print("Erro ao se conectar com o serviço de reconhecimento.")
