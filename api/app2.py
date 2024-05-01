from flask import Flask
import pika

app = Flask(__name__)

# Configurar la conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='chat_queue')


# Consumir mensajes de la cola
def callback(ch, method, properties, body):
    print("Mensaje recibido: %r" % body.decode())


channel.basic_consume(queue='chat_queue', on_message_callback=callback, auto_ack=True)


@app.route('/app2')
def app2_route():
    return 'Este es el servidor 2'


if __name__ == '__main__':
    # Iniciar la consumición de mensajes
    channel.start_consuming()
    app.run(debug=True, port=5002)
