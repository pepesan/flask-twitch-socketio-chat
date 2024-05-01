import bottle
import pika

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='my_queue')

# Configuración de la aplicación Bottle
app = bottle.Bottle()


@app.route('/mensajes', method='GET')
def obtener_mensajes():
    def generar_mensajes():
        method_frame, _, body = channel.basic_get(queue='my_queue', auto_ack=True)
        while method_frame:
            yield body
            method_frame, _, body = channel.basic_get(queue='my_queue', auto_ack=True)

    return bottle.HTTPResponse(generar_mensajes(), content_type='text/plain')


if __name__ == '__main__':
    bottle.run(app, host='localhost', port=5002)
