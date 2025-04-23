import os
import logging
from dotenv import load_dotenv
from flask_socketio import SocketIO, emit

from mqtt_shared import MQTTInitialData, ConnectionManager, Topics
from game_shared import DEVICE_TYPE, GAME_STATUS

from static.consts import LOGFILE

def close_connection():
    ConnectionManager.close_connection()

def create_connection(socketio : SocketIO) -> ConnectionManager:
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

    def on_message(conn, topic, data):
            if topic == Topics.STATE:
                future_page = body = None
                if data["state"] in [GAME_STATUS.DONE.value, GAME_STATUS.STOPPED.value]:
                    future_page = '/game/end'
                if data["state"] in [GAME_STATUS.ACTIVE.value, GAME_STATUS.HALTED.value]:
                    future_page = '/game/process'
                # print("pre-emit: ", future_page)
                socketio.emit('redirect', {"url": future_page})
            elif topic == Topics.CONTOURS:
                socketio.emit('contours', data)
            elif Topics.is_word_state(topic):
                socketio.emit('word', data)

    return ConnectionManager.initialize(init_data, DEVICE_TYPE.CONTROL, logger, on_message)
