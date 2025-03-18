import os
from flask import Flask
import atexit
import logging
from uuid import uuid4
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit

from mqtt_shared import MQTTInitialData, ConnectionManager, Topics
from game_shared import DEVICE_TYPE, GAME_STATUS

from utils.browser_helper import open_browser, close_browser
from static.consts import LOGFILE

from routes.gameroutes import game_routes
from routes.adminroutes import admin_routes

logging.basicConfig(filename=LOGFILE)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
load_dotenv(verbose=True, override=True)

init_data = MQTTInitialData(
    host = os.getenv("HOST"),
    port = os.getenv("PORT"),
    username = os.getenv("USERNAME"),
    password = os.getenv("PASSWORD")
)

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
    atexit.register(lambda: close_browser(env))

    return app

app = create_app()
socketio = SocketIO(app)

def on_message(conn, topic, data):
        if topic == Topics.STATE:
            future_page = body = None
            if data["state"] in [GAME_STATUS.DONE.value, GAME_STATUS.STOPPED.value]: future_page = '/game/end'

            body = {
                'game_status':conn.current_game_status,
                'matched_list': conn.matched_list
            }

            socketio.emit('redirect', {"url": future_page, "body": body})

conn_manager = ConnectionManager.initialize(init_data, DEVICE_TYPE.CONTROL, logger, on_message)


if __name__ == '__main__':
    socketio.run(port=5000)
