import os
from dotenv import load_dotenv
from twitchAPI.helper import first

# Carga las variables de entorno desde .env
load_dotenv()
from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent, SortMethod, TwitchAPIException, TwitchBackendException
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio

APP_ID = os.environ['TWITCH_CLIENT_ID']
APP_SECRET = os.environ['TWITCH_CLIENT_SECRET']
USER_SCOPE = [
    # leer el chat
    AuthScope.CHAT_READ,
    # escribir en el chat
    AuthScope.CHAT_EDIT,
    # mandar SO's (el usuario del bot debe ser moderador)
    AuthScope.MODERATOR_MANAGE_SHOUTOUTS,
    # leer followers (el usuario del bot debe ser moderador)
    AuthScope.MODERATOR_READ_FOLLOWERS]
TARGET_CHANNEL = os.environ['TWITCH_CHANNEL']
BOT_USERNAME = os.environ['TWITCH_USERNAME']
import chat

twitch = ""


async def get_user_last_video(channel_name, twitch):
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch.get_users(logins=channel_name))
    video_data = twitch.get_videos(user_id=user.id, first=1, sort=SortMethod.TIME)
    # cerrando la conexión
    await twitch.close()
    return video_data


async def get_user_last_stream(channel_name):
    twitch = await Twitch(APP_ID, APP_SECRET)
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch.get_users(logins=channel_name))
    video_data = twitch.get_streams(user_id=user.id, first=1)
    await twitch.close()
    return video_data


async def shoutout_from_to(channel_name):
    twitch = await Twitch(os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'])
    twitch.app_auth_refresh_callback = app_refresh
    twitch.user_auth_refresh_callback = user_refresh
    auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch.get_users(logins=channel_name))
    bot = await first(twitch.get_users(logins=BOT_USERNAME))
    streamer = await first(twitch.get_users(logins=TARGET_CHANNEL))
    await twitch.send_a_shoutout(streamer.id, user.id, bot.id)
    await twitch.close()


async def chat_so(channel_name, cmd):
    try:
        video_data = await get_user_last_video(channel_name)
        # print("Video")
        async for video in video_data:
            # print(video)
            # print(video.type)
            # print(video.title)
            # print(video.description)
            await cmd.reply(f"Echale un vistazo al canal de https://twitch.tv/{channel_name}."
                            f" El último video fue sobre: {video.title}")
            break
        stream_data = await get_user_last_stream(channel_name)
        print("Stream")
        async for stream in stream_data:
            print(stream)
            print(stream.title)
        # twitchAPI.types.UnauthorizedException: require user authentication!
        # await shoutout_from_to(cmd.parameter)
    except TwitchAPIException as t:
        print("An exception while consulting user")
        print(type(t))
        print(t)
        print(t.args)


async def user_refresh(token: str, refresh_token: str):
    print(f'my new user token is: {token}')


async def app_refresh(token: str):
    print(f'my new app token is: {token}')


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


# this will be called whenever the !reply command is issued
# async def test_command(cmd: ChatCommand):
#    print(cmd)
#    if len(cmd.parameter) == 0:
#        await cmd.reply('you did not tell me what to reply with')
#    else:
#        await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')

async def help_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply('Ayuda: puedes usar los comandos: !youtube !redes !java !angular !github !discord')


async def youtube_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply('El canal de Youtube es: https://www.youtube.com/@CursosdeDesarrollo , Canal secundario '
                    'https://www.youtube.com/@CursosDesencadenado')


async def redes_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply("Enlaces de contacto: https://twitter.com/dvaquero , https://twitter.com/CDDesarrollo y "
                    "https://www.linkedin.com/in/davidvaquero/")


async def java_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply("Este es el enlace al curso de java en Youtube: "
                    "https://www.youtube.com/watch?v=JExfQrDN03k&list=PLd7FFr2YzghOjHnoLF_yLjjOFnknA8qJj")


async def angular_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply("Este es el enlace al curso de angular en Youtube: "
                    "https://www.youtube.com/watch?v=UGBWmShB4J8&list=PLd7FFr2YzghNPi66KMyBbrBmJzH-RPYz0")


async def github_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply("El perfil de github es: https://github.com/pepesan")


async def discord_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply("El servidor de discord está en: https://discord.gg/9eWkvyR")


async def so_command(cmd: ChatCommand):
    # print(cmd)
    # print(cmd.user.name)
    # print(cmd.text)
    # print(cmd.parameter)
    channel_name = cmd.parameter
    try:
        print(twitch)
        await shoutout_from_to(channel_name)
        try:
            video_data = await get_user_last_video(channel_name, twitch)
            # print("Video")
            async for video in video_data:
                # print(video)
                # print(video.type)
                # print(video.title)
                # print(video.description)
                await cmd.reply(f"Echale un vistazo al canal de https://twitch.tv/{channel_name}."
                                f" El último video fue sobre: {video.title}")
                break
            stream_data = await get_user_last_stream(channel_name)
            print("Stream")
            async for stream in stream_data:
                print(stream)
                print(stream.title)
            # twitchAPI.types.UnauthorizedException: require user authentication!
            # await shoutout_from_to(cmd.parameter)
        except TwitchAPIException as t:
            print("An exception while getting user data")
            print(t)
    except TwitchAPIException as t:
        print("An exception while shoutouting")
        print(t)
    """
    await cmd.reply(f"/shoutout {channel_name}")
    """



# this is where we set up the bot
async def run():
    import chat
    # set up twitch api instance and add user authentication with some scopes
    twitch = await chat.get_chat_bot()
    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)
    # listen to channel subscriptions
    chat.register_event(ChatEvent.SUB, on_sub)
    # there are more events, you can view them all in this documentation
    chat.register_event(ChatEvent.RAID, on_raid)
    # you can directly register commands and their handlers, this will register the !reply command
    # chat.register_command('reply', test_command)
    chat.register_command('help', help_command)
    chat.register_command('youtube', youtube_command)
    chat.register_command('java', java_command)
    chat.register_command('angular', angular_command)
    chat.register_command('redes', redes_command)
    chat.register_command('discord', discord_command)
    chat.register_command('github', github_command)
    chat.register_command('so', so_command)
    # we are done with our setup, lets start this bot up!
    chat.start()

    # lets run till we press enter in the console
    try:
        input('press ENTER to stop\\n')
    finally:
        # now we can close the chat bot and the twitch api client
        chat.stop()
        await twitch.close()


if __name__ == '__main__':
    asyncio.run(run())
