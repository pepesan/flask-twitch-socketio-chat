from twitchAPI.helper import first
from twitchAPI.types import SortMethod, TwitchAPIException
import os
from dotenv import load_dotenv
import chat_bot
from chat_bot.bot_class import TARGET_CHANNEL, BOT_USERNAME

# Carga las variables de entorno desde .env
load_dotenv()




async def get_user_last_video(channel_name, twitch_object):
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch_object.get_users(logins=channel_name))
    video_data = twitch_object.get_videos(user_id=user.id, first=1, sort=SortMethod.TIME)
    # cerrando la conexión
    await twitch_object.close()
    return video_data


async def get_user_last_stream(channel_name, twitch_object):
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch_object.get_users(logins=channel_name))
    video_data = twitch_object.get_streams(user_id=user.id, first=1)
    await twitch_object.close()
    return video_data


async def shoutout_from_to(channel_name, twitch):
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch.get_users(logins=channel_name))
    bot = await first(twitch.get_users(logins=BOT_USERNAME))
    streamer = await first(twitch.get_users(logins=TARGET_CHANNEL))
    await twitch.send_a_shoutout(streamer.id, user.id, bot.id)
    await twitch.close()


async def chat_so(channel_name, cmd, twitch_object):
    try:
        video_data = await get_user_last_video(channel_name, twitch_object)
        # print("Video")
        async for video in video_data:
            # print(video)
            # print(video.type)
            # print(video.title)
            # print(video.description)
            await cmd.reply(f"Echale un vistazo al canal de https://twitch.tv/{channel_name} ."
                            f" El último video fue sobre: {video.title}")
            break
        stream_data = await get_user_last_stream(channel_name, twitch_object)
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

