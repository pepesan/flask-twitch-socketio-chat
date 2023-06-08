import sys
import os
import pytube


def verificar_argumento():
    if len(sys.argv) < 2:
        print("Se requiere al menos un argumento.")
        sys.exit(1)


def cambiar_nombre_mp4_a_mp3(ruta_archivo):
    try:
        nuevo_nombre = os.path.splitext(ruta_archivo)[0] + ".mp3"
        os.rename(ruta_archivo, nuevo_nombre)
        print("Cambio de nombre completado.")
        return nuevo_nombre
    except Exception as e:
        print("Ocurrió un error durante el cambio de nombre:", str(e))


def cambiar_nombre_mp3_a_wav(ruta_archivo):
    try:
        nuevo_nombre = os.path.splitext(ruta_archivo)[0] + ".wav"
        print("Cambio de nombre completado.")
        return nuevo_nombre
    except Exception as e:
        print("Ocurrió un error durante el cambio de nombre:", str(e))


def convertir_mp3_a_wav(ruta_archivo_mp3, ruta_archivo_wav):
    import ffmpeg
    try:
        stream = ffmpeg.input(ruta_archivo_mp3)
        stream = ffmpeg.output(stream, ruta_archivo_wav, format='wav')
        ffmpeg.run(stream)
        print("Conversión de MP3 a WAV completada.")
    except Exception as e:
        print("Ocurrió un error durante la conversión:", str(e))


def main():
    argumento = sys.argv[1]
    print("El argumento pasado es:", argumento)
    try:
        # YouTube(argumento).streams.first().download()
        from pytube import YouTube
        import ffmpeg

        video = pytube.YouTube(sys.argv[1])
        audio = video.streams.filter(only_audio=True).first()
        ruta_descarga = audio.download()
        print("descargado: ")
        print(ruta_descarga)
        ruta_mp3 = cambiar_nombre_mp4_a_mp3(ruta_descarga)
        ruta_wav = cambiar_nombre_mp3_a_wav(ruta_mp3)
        convertir_mp3_a_wav(ruta_mp3, ruta_wav)
        print("Descarga y conversión a WAV sin comprimir completadas.")
    except Exception as e:
        print("Ocurrió un error durante la descarga o conversión:", str(e))


if __name__ == "__main__":
    verificar_argumento()
    main()
