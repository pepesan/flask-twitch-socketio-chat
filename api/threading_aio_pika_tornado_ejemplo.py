import threading
import aio_pika
import tornado.ioloop
import tornado.web


def consume_from_queue(queue_name):
    async def consume():
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

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(consume())


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("¡Hola desde Tornado!")


def start_tornado():
    application = tornado.web.Application([(r"/", MainHandler)])
    application.listen(8888)  # Puerto en el que se ejecutará el servidor Tornado
    tornado.ioloop.IOLoop.current().start()


def main():
    threading.Thread(target=start_tornado).start()
    threading.Thread(target=consume_from_queue, args=("my_queue",)).start()


main()
