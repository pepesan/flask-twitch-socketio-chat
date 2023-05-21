import os
from dotenv import load_dotenv

from twitchAPI.chat import EventData, ChatMessage, ChatSub
from twitchAPI.types import ChatEvent

import pyaudio
import wave
from TTS.api import TTS

load_dotenv()


def prepare_sounds_folder():
    if os.environ['TTS_SOUND_FOLDER']:
        folder_name = os.environ['TTS_SOUND_FOLDER']
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
            print(f"Folder '{folder_name}' created successfully.")
        else:
            print(f"Folder '{folder_name}' already exists.")


## cargando el TTS
if os.environ['TTS_ACTIVATE']:
    if os.environ['TTS_LANGUAGE'] == "es":
        model_name = os.environ['TTS_MODEL_ES']
    else:
        model_name = os.environ['TTS_MODEL']
    tts = TTS(model_name=model_name, progress_bar=True, gpu=True)


def text_to_tts(text, tts):
    prepare_sounds_folder()
    if os.environ['TTS_MULTILANGUAGE'] == True:
        # en base a un wav propio
        tts.tts_to_file(text,
            speaker_wav=f"{os.environ['TTS_SOUND_FOLDER']}/muestra.wav",
            language=os.environ['TTS_LANGUAGE'],
            file_path=f"{os.environ['TTS_SOUND_FOLDER']}/salida.wav")
    else:
        if os.environ['TTS_LANGUAGE'] == "es":
            tts.tts_to_file(text=text, file_path="salida.wav")
        else:
            # en base a un wav propio
            tts.tts_to_file(
                text,
                speaker_wav=f"{os.environ['TTS_SOUND_FOLDER']}/muestra.wav",
                file_path=f"{os.environ['TTS_SOUND_FOLDER']}/salida.wav")

    if os.environ['TTS_VOCODER'] == True:
        tts.voice_conversion_to_file(
            source_wav=f"{os.environ['TTS_SOUND_FOLDER']}/muestra.wav",
            target_wav=f"{os.environ['TTS_SOUND_FOLDER']}/intermedia.wav",
            file_path="output.wav")
        # Join the source file path and destination folder path to create the new file path
        new_file_path = os.path.join(os.environ['TTS_SOUND_FOLDER'], os.path.basename("salida.wav"))

        # Rename the file to move it to the destination folder
        os.rename(f"{os.environ['TTS_SOUND_FOLDER']}/output.wav", new_file_path)

    # define stream chunk
    chunk = 1024

    # open a wav format music
    f = wave.open(r"salida.wav", "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()


# this will be called when the event READY is triggered, which will be on bot start
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    # join our target channel, if you want to join multiple, either call join for each individually
    # or even better pass a list of channels as the argument
    await ready_event.chat.join_room(os.environ['TWITCH_CHANNEL'])
    # you can do other bot initialization things in here


# this will be called whenever a message in a channel was send by either the bot OR another user
async def on_message(msg: ChatMessage):
    print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')
    if os.environ['TTS_ACTIVATE']==True:
        if msg.user.name != os.environ['TWITCH_USERNAME']:
            text_to_tts(f'{msg.text}', tts)
        else:
            text_to_tts(f'{msg.user.name} {os.environ["TTS_SAID_TEXT"]}: {msg.text}', tts)

# this will be called whenever someone subscribes to a channel
async def on_sub(sub: ChatSub):
    print(sub)
    print(f'New subscription in {sub.room.name}:\\n'
          f'  Type: {sub.sub_plan}\\n'
          f'  Message: {sub.sub_message}')


async def on_raid(raid: ChatEvent):
    print(f"New Raid: {raid}")
    print(raid)
    print(raid.__dict__)
