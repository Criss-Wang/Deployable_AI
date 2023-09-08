from flask import Flask
from flask_socketio import SocketIO 

from client import client

socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "secret"

    app.register_blueprint(client)

    socketio.init_app(app)

    return app
