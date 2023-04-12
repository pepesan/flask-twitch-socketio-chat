from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
import asyncio
from dotenv import load_dotenv
import os

from twitchAPI.types import SortMethod

streamer = "cursosdedesarrollo"

# Carga las variables de entorno desde .env
load_dotenv()


async def twitch_example(streamer):
    # initialize the twitch instance, this will by default also create a app authentication for you
    twitch = await Twitch(os.environ['TWITCH_CLIENT_ID'], os.environ['TWITCH_CLIENT_SECRET'])
    # call the API for the data of your twitch user
    # this returns a async generator that can be used to iterate over all results
    # but we are just interested in the first result
    # using the first helper makes this easy.
    user = await first(twitch.get_users(logins=streamer))
    # print the ID of your user or do whatever else you want with it
    print(user.id)
    print(user.display_name)
    print(user.description)
    print(user.broadcaster_type)
    print(user.profile_image_url)
    video_data = twitch.get_videos(user_id=user.id, first=10, sort=SortMethod.TIME)
    print(video_data)

    async for video in video_data:
        print(video)
        print(video.type)
        print(video.title)
        print(video.description)

    video_data = twitch.get_streams(user_id=user.id, first=1)
    print("streams")
    async for video in video_data:
        print(video)
        print(video.type)
        print(video.title)
        print(video.description)
    await twitch.close()


# run this example
asyncio.run(twitch_example(streamer))

