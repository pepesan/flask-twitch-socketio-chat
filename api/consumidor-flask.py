import gevent
from flask import Flask, Response
from flask_sse import sse
import pika
from gevent import monkey

monkey.patch_all()

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='my_queue')

# Configuración de la aplicación Flask
app = Flask(__name__)
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/mensajes')
def obtener_mensajes():
    def recibir_mensajes():
        method_frame, _, body = channel.basic_get(queue='my_queue', auto_ack=True)
        while method_frame:
            with app.app_context():
                sse.publish(body.decode(), type='mensaje')
            method_frame, _, body = channel.basic_get(queue='my_queue', auto_ack=True)

    gevent.spawn(recibir_mensajes)
    return Response('', content_type='text/event-stream')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
