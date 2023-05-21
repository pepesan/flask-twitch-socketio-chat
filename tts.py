#!usr/bin/env python
# coding=utf-8

import pyaudio
import wave
from TTS.api import TTS

if __name__ == '__main__':
    # Seleción del modelo
    model_name = "tts_models/es/css10/vits"
    # carga del modelo
    tts = TTS(model_name=model_name, progress_bar=False, gpu=True)
    # conversión de texto a voz en fichero WAV
    tts.tts_to_file(text="Necesitamossh máquinasshh que construyan máquinasssh", file_path="salida.wav")
    # en base a un wav propio
    #tts.tts_to_file("buenas noches gente", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")



    ## Reproducción del audio

    #define stream chunk
    chunk = 1024

    #open a wav format music
    f = wave.open(r"salida.wav","rb")
    #instantiate PyAudio
    p = pyaudio.PyAudio()
    #open stream
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
                    channels = f.getnchannels(),
                    rate = f.getframerate(),
                    output = True)
    #read data
    data = f.readframes(chunk)

    #play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    #stop stream
    stream.stop_stream()
    stream.close()

    #close PyAudio
    p.terminate()