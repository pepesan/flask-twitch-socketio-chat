import threading
import json
import pika
import tornado.ioloop
import tornado.web

mensajes = []

def consume_from_queue(queue_name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")  # Cambia la URL de conexión según tu configuración de RabbitMQ
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        print("Mensaje recibido:", body.decode())
        mensajes.append(body.decode())
        print("mensajes: ", mensajes)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(mensajes))


def start_tornado():
    application = tornado.web.Application([(r"/", MainHandler)])
    application.listen(8888)  # Puerto en el que se ejecutará el servidor Tornado
    tornado.ioloop.IOLoop.current().start()


def main():
    threading.Thread(target=start_tornado).start()
    threading.Thread(target=consume_from_queue, args=("my_queue",)).start()


main()
