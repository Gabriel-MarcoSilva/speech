import speech_recognition as sr

# Inicializa o reconhecedor de fala
recognizer = sr.Recognizer()

# Captura áudio do microfone
with sr.Microphone() as source:
    print("Ajustando o nível de ruído... Fale agora!")
    recognizer.adjust_for_ambient_noise(source)  # Ajusta o nível de ruído ambiente
    print("Fale algo...")
    
    # Captura áudio até detectar uma pausa
    audio = recognizer.listen(source, phrase_time_limit=10)  # O tempo máximo de captura é de 10 segundos

# Usa o Google Web Speech API para transcrever o áudio
try:
    print("Reconhecendo...")
    text = recognizer.recognize_google(audio, language='pt-BR')  # Usando o idioma português do Brasil
    print("Texto reconhecido: " + text)

except sr.UnknownValueError:
    print("Não foi possível entender o áudio")
except sr.RequestError:
    print("Erro na solicitação ao serviço de reconhecimento de fala")
