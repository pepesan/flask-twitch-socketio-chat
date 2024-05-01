import asyncio
import aio_pika
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/messages', methods=['POST'])
def receive_message():
    message = request.json['message']
    # Hacer algo con el mensaje recibido en la API REST, como almacenarlo en una base de datos
    print(f"Mensaje recibido en la API REST: {message}")
    return 'Mensaje recibido en la API REST'

async def consume():
    # Establecer la conexión con el servidor RabbitMQ
    connection = await aio_pika.connect_robust("amqp://localhost/")

    # Crear un canal de comunicación
    channel = await connection.channel()

    # Declarar una cola
    queue = await channel.declare_queue("my_queue")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print("procesando mensaje")
                # Obtener el cuerpo del mensaje
                body = message.body.decode()

                # Hacer algo con el mensaje
                print(f"Mensaje recibido en RabbitMQ: {body}")

                # Publicar el mensaje en la API REST
                url = 'http://localhost:5000/messages'
                payload = {'message': body}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, json=payload, headers=headers)
                print(f"Respuesta de la API REST: {response.text}")

                # Romper el ciclo si recibimos un mensaje especial
                if body == "salir":
                    break

    # Cerrar la conexión
    await connection.close()

# Ejecutar la función de consumo de forma asíncrona
asyncio.ensure_future(consume())

# Ejecutar la API REST en el mismo servidor
if __name__ == '__main__':
    app.run()
