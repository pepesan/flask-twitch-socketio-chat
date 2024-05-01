import tornado.ioloop
import tornado.web
import tornado.websocket
import json


class MainHandler(tornado.web.RequestHandler):
    data = []
    websocket_clients = set()

    def get(self):
        self.render("./static/websocket_tornado.html")

    def post(self):
        try:
            new_item = json.loads(self.request.body)
            if isinstance(new_item, str):
                self.data.append(new_item)
                self.write("Dato agregado correctamente.")
                self.send_message_to_websockets(new_item)
            else:
                self.set_status(400)
                self.write("Error: Se esperaba una cadena JSON.")
        except Exception as e:
            self.set_status(500)
            self.write(f"Error interno del servidor: {str(e)}")

    @classmethod
    def send_message_to_websockets(cls, message):
        for client in cls.websocket_clients:
            client.write_message(message)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        MainHandler.websocket_clients.add(self)
        self.write_message(json.dumps(MainHandler.data))

    def on_close(self):
        MainHandler.websocket_clients.remove(self)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", WebSocketHandler),
    ], static_path='')


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
