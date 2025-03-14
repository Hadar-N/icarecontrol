import os
from flask import Flask
import atexit
import logging
from dotenv import load_dotenv

from mqtt_shared import MQTTInitialData, ConnectionManager
from game_shared import DEVICE_TYPE
from utils.browserHelper import open_browser, close_browser
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

conn_manager = ConnectionManager.initialize(init_data, DEVICE_TYPE.CONTROL, logger)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    app.register_blueprint(game_routes)
    app.register_blueprint(admin_routes)

    env = os.getenv("ENV", "pi")
    url = "http://127.0.0.1:5000/game/"
    open_browser(env, url)
    atexit.register(lambda: close_browser(env))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=5000)