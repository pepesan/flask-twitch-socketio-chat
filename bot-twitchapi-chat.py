from dotenv import load_dotenv
from chat_bot.chat_bot import get_chat_bot
from chat_bot.commands import help_command, youtube_command, java_command, angular_command, redes_command, \
    discord_command, github_command, so_command, javaweb_command, typescript_command, grabando_command
from events import on_ready, on_message, on_sub, on_raid

# Carga las variables de entorno desde .env
load_dotenv()
from twitchAPI.types import ChatEvent
from twitchAPI.chat import Chat
import asyncio


async def run():
    twitch = await get_chat_bot("")
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
    chat.register_command('grabando', grabando_command)
    chat.register_command('java', java_command)
    chat.register_command('javaweb', javaweb_command)
    chat.register_command('typescript', typescript_command)
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
