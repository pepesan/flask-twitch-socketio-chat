import asyncio
import json

from aiohttp import web

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage

mensajes = []


def get_variable_type(variable):
    return type(variable).__name__


async def on_message(message: AbstractIncomingMessage) -> None:
    """
    on_message doesn't necessarily have to be defined as async.
    Here it is to show that it's possible.
    """
    print(" [x] Received message %r" % message)
    print("Message body is: %r" % message.body)
    print("Message body type is: %r" % get_variable_type(message.body))
    mensajes.append(message.body.decode())
    print(mensajes)
    # print("Before sleep!")
    # await asyncio.sleep(5)  # Represents async I/O operations
    # print("After sleep!")


async def main() -> None:
    # Perform connection
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue("my_queue")

        # Start listening the queue with name 'hello'
        await queue.consume(on_message, no_ack=True)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def handle_messages(request):
    return web.Response(text=json.dumps(mensajes))


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/msg', handle_messages),
                web.get('/{name}', handle),
                ])

if __name__ == '__main__':
    asyncio.run(main())
    web.run_app(app)

