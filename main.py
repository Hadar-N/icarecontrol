import os
from functools import partial
from flask import Flask
import atexit
from uuid import uuid4
from flask_socketio import SocketIO, emit

from utils.browser_helper import open_browser, close_browser
from utils.create_connection import create_connection, close_connection
from utils.speech_single import SpeechSingle
from routes.gameroutes import game_routes
from routes.adminroutes import admin_routes

def on_exit(env):
    close_browser(env)
    SpeechSingle.stop()
    close_connection()

def create_app():
    device_id = uuid4()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config['DEVICE_ID'] = device_id.__str__()

    app.register_blueprint(game_routes)
    app.register_blueprint(admin_routes)

    env = os.getenv("ENV", "pi")
    url = "http://127.0.0.1:5000/game/"
    open_browser(env, url)
    atexit.register(partial(on_exit, env))

    return app

app = create_app()
socketio = SocketIO(app)
conn_manager = create_connection(socketio)

if __name__ == '__main__':
    socketio.run(port=5000)
