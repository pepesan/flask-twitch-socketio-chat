from pytube import YouTube, Channel, Playlist
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
    # main()
    # Encuentra el canal de YouTube que quieres descargar.
    # channel_id = "UChE59MSKV-eEFyS-0_wqrFg"
    channel_url = sys.argv[1]
    # Obtén la lista de listas de reproducción del canal.
    channel = Channel(channel_url)
    channel_id = channel.channel_id
    print(channel_id)
    video_urls = channel.videos
    for url in video_urls[:3]:
        print(url)
    #
    # # Itera sobre las listas de reproducción.
    # for playlist in playlists:
    #
    #     # Obtén la URL de la lista de reproducción.
    #     playlist_url = playlist.url
    #
    #     # Obtén los vídeos de la lista de reproducción.
    #     videos = playlist.videos
    #
    #     # Itera sobre los vídeos.
    #     for video in videos:
    #         # Descarga el vídeo en formato MP4.
    #         video.set_filename(video.title + ".mp4")
    #         video.download()
