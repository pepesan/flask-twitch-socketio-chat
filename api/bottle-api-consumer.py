from bottle import Bottle, request, response, run
import pika

# Configurar la conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='chat_queue')


def callback(ch, method, properties, body):
    print("mensaje recibido")
    print("Mensaje recibido: %r" % body.decode())


channel.basic_consume(queue='chat_queue', on_message_callback=callback, auto_ack=True)

app = Bottle()


# Ruta para la solicitud GET
@app.get('/api/chat')
def chat():
    message = 'Hola, mundo!'
    return {'mensaje': 'Mensaje enviado'}


# Ruta para la solicitud POST
@app.post('/api/data')
def save_data():
    data = request.json  # Obtener los datos JSON enviados en el cuerpo de la solicitud
    # Aquí puedes realizar la lógica para guardar los datos recibidos
    return {'status': 'OK'}


if __name__ == '__main__':
    run(app, host='localhost', port=5002)
