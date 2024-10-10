# main.py
import whisper
from os import path

model = whisper.load_model('large')

def get_transcribe(audio: str, language: str = 'fr'):
    return model.transcribe(audio=audio, language=language, verbose=True)

if __name__ == "__main__":
    result = get_transcribe(audio = "input/example.wav")
    print('-'*50)
    print(result.get('text', ''))