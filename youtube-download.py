from pytube import YouTube
import sys


def verificar_argumento():
    if len(sys.argv) < 2:
        print("Se requiere al menos un argumento.")
        sys.exit(1)


def main():
    argumento = sys.argv[1]
    print("El argumento pasado es:", argumento)
    # YouTube(argumento).streams.first().download()
    yt = YouTube(argumento)
    yt \
        .streams \
        .filter(progressive=True, file_extension='mp4') \
        .order_by('resolution') \
        .desc() \
        .first() \
        .download(output_path="./videos")


if __name__ == "__main__":
    verificar_argumento()
    main()
