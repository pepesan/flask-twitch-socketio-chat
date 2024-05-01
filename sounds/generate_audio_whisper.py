import whisper
import sys
import os
from datetime import timedelta
def verificar_argumento():
    if len(sys.argv) < 2:
        print("Se requiere al menos un argumento.")
        sys.exit(1)

from datetime import timedelta
import os
import whisper

def transcribe_audio(path, model_name):
    model = whisper.load_model(model_name) # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1

        # Obtener el nombre del archivo de audio sin la extensión
        audioFilename = os.path.splitext(os.path.basename(path))[0]

        # Generar el nombre del archivo SRT
        srtFilename = os.path.join("SrtFiles", f"{audioFilename}.srt")

        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n")

    return srtFilename

argumento = sys.argv[1]
transcribe_audio(argumento, "large")
