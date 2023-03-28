from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import os
import logging
from dotenv import load_dotenv

# Carga las variables de entorno desde .env
load_dotenv()

from twitchio.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        print("iniciando cliente de twitch")
        super().__init__(token=os.environ['TWITCH_ACCESS_TOKEN'], prefix='!',
                         initial_channels=['cursosdedesarrollo', 'chrisvdev'])

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
        #print(message.author)
         #print(message.channel)
        #print(message.raw_data)
        #print(message.id)
        #print(message.tags)

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
    async def eseo(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'sigan a chrisdev que es un máquina')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.logger.setLevel(logging.INFO)
socketio = SocketIO(app, cors_allowed_origins="*")
bot = Bot()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hello/<string:name>')
async def hello_name(name):
    print(name)
    await bot.sendMessage("Suerte!")
    return f'Hola {name}!'

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)
    emit('response', 'Server received message: ' + message)


import threading
# Iniciar el bot de Twitch en un hilo separado
bot_thread = threading.Thread(target=bot.run)
bot_thread.start()

if __name__ == '__main__':

    # Iniciar Flask y SocketIO en un hilo
    socketio_thread = threading.Thread(target=socketio.run, args=(app,))
    socketio_thread.start()

    #bot.run()


