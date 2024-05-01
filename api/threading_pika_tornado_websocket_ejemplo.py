import threading
import json
import pika
import tornado.ioloop
import tornado.web
import tornado.websocket

mensajes = []
websocket_connections = []


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
        for connection in websocket_connections:
            connection.write_message(body.decode())

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(mensajes))


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Nueva conexión WebSocket abierta")
        websocket_connections.append(self)

    def on_message(self, message):
        # No es necesario en este caso, ya que solo se recibirán mensajes del servidor
        pass

    def on_close(self):
        print("Conexión WebSocket cerrada")
        websocket_connections.remove(self)


class MessageHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(mensajes))


def start_tornado():
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WebSocketHandler),  # Ruta para WebSocket
        (r"/msg", MessageHandler)  # Ruta para obtener los mensajes en formato JSON
    ])
    application.listen(8888)  # Puerto en el que se ejecutará el servidor Tornado
    tornado.ioloop.IOLoop.current().start()


def main():
    threading.Thread(target=start_tornado).start()
    threading.Thread(target=consume_from_queue, args=("my_queue",)).start()


main()
