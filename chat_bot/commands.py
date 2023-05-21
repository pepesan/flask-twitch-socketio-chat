from twitchAPI.chat import ChatCommand
from twitchAPI.types import TwitchAPIException

from chat_bot import chat_bot
from chat_bot.api_service import shoutout_from_to, chat_so, get_user_last_stream


async def help_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply('Ayuda: puedes usar los comandos: !youtube !redes !java !javaweb !angular !github !discord')


async def grabando_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply('Estamos grabando un curso para Youtube. Mientras tanto no podemos atender al chat. Cuando '
                    'terminemos podemos atender tus preguntas.')


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


async def javaweb_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply("Este es el enlace al curso de java Web en Youtube: "
                    "https://www.youtube.com/playlist?list=PLd7FFr2YzghNRITcQTMsuW5puOPGH3-PV")


async def typescript_command(cmd: ChatCommand):
    # print(cmd)
    await cmd.reply("Este es el enlace al curso de Typescript en Youtube "
                    "y el repositorio de código: "
                    "https://github.com/pepesan/curso-typescript-twitch")


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
        twitch = await chat_bot.get_chat_bot("")
        try:
            await shoutout_from_to(channel_name, twitch)
        except TwitchAPIException as t:
            print("An exception while getting user data")
            print(t)
        await chat_so(channel_name, cmd, twitch)
        try:
            stream_data = await get_user_last_stream(channel_name, twitch)
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
