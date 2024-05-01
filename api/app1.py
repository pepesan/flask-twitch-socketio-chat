from flask import Flask, jsonify
import pika

app = Flask(__name__)

# Configurar la conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='chat_queue')


@app.route('/api/chat', methods=['GET'])
def chat():
    # Publicar un mensaje en la cola
    message = 'Hola, mundo!'
    channel.basic_publish(exchange='', routing_key='chat_queue', body=message)

    return jsonify({'mensaje': 'Mensaje enviado'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
