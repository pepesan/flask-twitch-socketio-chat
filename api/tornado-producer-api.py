import tornado.ioloop
import tornado.web
import tornado.log
import pika

tornado.log.enable_pretty_logging()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # Conexión a RabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='my_queue')
        msg = "mensaje"
        channel.basic_publish(exchange='', routing_key='my_queue', body=msg.encode())
        tornado.log.app_log.info(f"mensaje publicado %s", msg)
        connection.close()
        self.write("Hello, world")


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
