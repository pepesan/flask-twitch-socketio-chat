import os
import threading
import json
import pika
import tornado.ioloop
import tornado.web
import tornado.websocket

mensajes = []
websocket_connections = []


class QueueConsumer:

    def __init__(self, queue_name):
        global websocket_connections
        self.websocket_connections = websocket_connections
        global mensajes
        self.mensajes = mensajes
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def start_consuming(self):
        print("empiezo a consumir")
        self.connection = pika.SelectConnection(
            pika.ConnectionParameters("localhost"),  # Cambia la URL de conexión según tu configuración de RabbitMQ
            on_open_callback=self.on_connection_open
        )
        self.connection.ioloop.start()

    def on_connection_open(self, connection):
        connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.queue_declare(queue=self.queue_name, callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.on_message, auto_ack=True)

    def on_message(self, channel, method, properties, body):
        print("Mensaje recibido:", body.decode())
        self.mensajes.append(body.decode())
        print("mensajes:", self.mensajes)
        for connection in self.websocket_connections:
            print("tipo de connection: ", type(connection))
            mijson = json.dumps({
                "mensaje": body.decode()
            })
            print("mensaje a enviar:  ", mijson)
            connection.write_message(mijson)

    def stop_consuming(self):
        if self.connection is not None and self.connection.is_open:
            self.connection.close()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(mensajes))


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, application, request, **handler_kwargs):
        super().__init__(application, request, **handler_kwargs)
        global mensajes
        global websocket_connections
        self.mensajes = mensajes
        self.websocket_connections = websocket_connections

    def open(self):
        print("Nueva conexión WebSocket abierta")
        self.write_message("Bienvenid@")
        websocket_connections.append(self)

    def on_message(self, message):
        if message.startswith("GET"):
            # La cadena es una solicitud GET
            # Realiza aquí la acción que deseas realizar

            # Por ejemplo, imprimir la cadena de solicitud
            print("Solicitud GET recibida:", message)
            # O realizar una operación específica para las solicitudes GET
            # ...

        else:
            # La cadena no es una solicitud GET
            # Realiza aquí alguna acción alternativa

            # Por ejemplo, imprimir un mensaje de advertencia
            print("Mensaje recibido:", message)

        # definición del mensaje
        mensaje = {
            "mensajes": mensajes
        }
        # self.write_message(json.dumps(mensaje))  # Envía el mismo mensaje de vuelta al cliente
        for connection in self.websocket_connections:
            print("tipo de connection: ", type(connection))
            mijson = json.dumps({
                "mensaje": mensaje
            })
            print("mensaje a enviar:  ", mijson)
            connection.write_message(mijson)

    def on_close(self):
        print("Conexión WebSocket cerrada")
        websocket_connections.remove(self)

    def forceful_close(self):
        # Forzar el envío de mensajes encolados antes de cerrar la conexión
        while self._write_buffer:
            self._write_buffer.pop(0).callback(None)


class MessageHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(mensajes))


def start_tornado():
    tornado_port = 8888
    print(f"Arrancando el servidor Tornado en el puerto {tornado_port}.")
    static_path = os.path.join(os.path.dirname(__file__), "static")
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WebSocketHandler),  # Ruta para WebSocket
        (r"/msg", MessageHandler),  # Ruta para obtener los mensajes en formato JSON
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": static_path})  # Ruta para los archivos estáticos
    ])
    application.listen(8888)  # Puerto en el que se ejecutará el servidor Tornado
    tornado.ioloop.IOLoop.current().start()


def main():
    threading.Thread(target=start_tornado).start()
    queue_consumer = QueueConsumer("my_queue")
    threading.Thread(target=queue_consumer.start_consuming).start()


main()
