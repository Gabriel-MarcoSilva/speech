import os
import pyaudio
import time
from google.cloud import speech

# Defina o caminho para as credenciais do Google Cloud (se necessário)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'C:/Users/gabri/Documents/speech-to-text/chave.json'

# Configuração do cliente para o Google Cloud Speech-to-Text
client = speech.SpeechClient()

# Configurações de reconhecimento
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,  # Taxa de amostragem para o microfone (ajuste se necessário)
    language_code="pt-BR",  # Idioma de transcrição (ajuste conforme necessário)
)

# Configuração para reconhecimento em tempo real
streaming_config = speech.StreamingRecognitionConfig(config=config)

# Função para capturar e transcrever áudio em tempo real
def stream_transcribe(max_duration=10):
    # Configuração do PyAudio para capturar o áudio do microfone
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=16000,
                    input=True,
                    frames_per_buffer=1024)

    print(f"Iniciando transcrição... Fale algo! (tempo limite: {max_duration} segundos)")

    # Guarda o momento de início da transcrição
    start_time = time.time()

    # Função para gerar pacotes de áudio, respeitando o tempo limite
    def audio_stream():
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > max_duration:
                break
            yield stream.read(1024)

    # Gere os pedidos de áudio, que serão enviados à API em tempo real
    requests = (speech.StreamingRecognizeRequest(audio_content=content)
                for content in audio_stream())

    # Faça a chamada para o streaming de reconhecimento
    responses = client.streaming_recognize(streaming_config, requests)

    # Processa as respostas da transcrição
    try:
        for response in responses:
            for result in response.results:
                # Exibe a transcrição final ou parcial
                print("Texto reconhecido: ", result.alternatives[0].transcript)
    except Exception as e:
        print(f"Erro durante a transcrição: {e}")

    # Encerra o stream do microfone
    stream.stop_stream()
    stream.close()

# Chama a função para transcrição em tempo real
stream_transcribe(max_duration=10)
