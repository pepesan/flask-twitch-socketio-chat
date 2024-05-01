import asyncio
import aio_pika
from flask import Flask


async def consume_from_queue(queue_name):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost/",  # Cambia la URL de conexión según tu configuración de RabbitMQ
        loop=loop
    )

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print("Mensaje recibido:", message.body.decode())


app = Flask(__name__)


@app.route("/")
def hello():
    return "¡Hola desde Flask!"


async def tarea1():
    print("Tarea 1 iniciada")
    await consume_from_queue("my_queue")
    print("Tarea 1 completada")


async def tarea2():
    print("Tarea 2 iniciada")
    app.run()  # Arrancar el servidor Flask
    print("Tarea 2 completada")


async def main():
    tarea1_coro = tarea1()
    tarea2_coro = tarea2()

    await asyncio.gather(tarea1_coro, tarea2_coro)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
