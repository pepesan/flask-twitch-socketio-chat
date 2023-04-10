import os
from dotenv import load_dotenv
from twitchio.ext import commands

streamers = ['cursosdedesarrollo']


def find_if_streamer_is_sender(streamer):
    if streamer in streamers:
        return True
    else:
        return False


# Carga las variables de entorno desde .env
load_dotenv()


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        print("iniciando cliente de twitch")
        super().__init__(token=os.environ['TWITCH_ACCESS_TOKEN'], prefix='!',
                         initial_channels=['cursosdedesarrollo', 'chrisvdev', 'viciostv'])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print("conectado")
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        print(message.author, ": ", message.content)
        # print(message.author)
        # print(message.channel)
        # print(message.raw_data)
        # print(message.id)
        # print(message.tags)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def help(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Ayuda: puedes usar los comandos: !youtube !redes !java !angular !github !discord')

    @commands.command()
    async def youtube(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"El canal de Youtube es: https://www.youtube.com/@CursosdeDesarrollo"
                       f" , Canal secundario https://www.youtube.com/@CursosDesencadenado")

    @commands.command()
    async def java(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(
            f"Este es el enlace al curso de java en Youtube: "
            f"https://www.youtube.com/watch?v=JExfQrDN03k&list=PLd7FFr2YzghOjHnoLF_yLjjOFnknA8qJj")

    @commands.command()
    async def angular(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(
            f"Este es el enlace al curso de angular en Youtube: "
            f"https://www.youtube.com/watch?v=UGBWmShB4J8&list=PLd7FFr2YzghNPi66KMyBbrBmJzH-RPYz0")

    @commands.command()
    async def redes(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"Enlaces de contacto: https://twitter.com/dvaquero , https://twitter.com/CDDesarrollo y "
                       f"https://www.linkedin.com/in/davidvaquero/")

    @commands.command()
    async def discord(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"El servidor de discord está en: https://discord.gg/9eWkvyR")

    @commands.command()
    async def github(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"El perfil de github es: https://github.com/pepesan")

    @commands.command()
    async def so(self, ctx: commands.Context):
        # print(ctx.author.name)
        # print(type(ctx.author.name))
        if find_if_streamer_is_sender(ctx.author.name):
            # print("imprimiendo")
            try:
                channel_name = ctx.message.content.split(" ")[1]
                await ctx.send(f'Echale un vistazo al canal de https://twitch.tv/{channel_name}')
                # print("mandado")
            except Exception as e:
                # print("excepción")
                # Manejo de cualquier excepción
                print("Se produjo una excepción:", type(e).__name__)


if __name__ == '__main__':
    bot = Bot()
    bot.run()
