import bottle
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='my_queue')

app = bottle.Bottle()


@app.route('/message/<msg>')
def produce_message(msg):

    channel.basic_publish(exchange='', routing_key='my_queue', body=msg)
    # connection.close()
    return "Mensaje enviado: {}".format(msg)


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
