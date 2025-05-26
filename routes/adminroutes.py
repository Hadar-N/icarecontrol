import time
import re
import json
from flask import request, session, Blueprint
from dataclasses import asdict

from mqtt_shared import ConnectionManager, Topics
from game_shared import GAME_LEVELS, GAME_MODES, MQTT_COMMANDS

from static.consts import SUCCESS_RES, ARRAY_STR_DETECTOR
from utils.curr_data_single import CurrDataSingle
from utils.speech_single import SpeechSingle

admin_routes = Blueprint('adm', __name__)

conn_manager = ConnectionManager.get_instance()
data_singleton = CurrDataSingle()
speech_singleton = SpeechSingle()

@admin_routes.route('/speak', methods=['POST'])
def speak():
    word = request.json.get('word')
    if isinstance(word, str) and re.search(ARRAY_STR_DETECTOR, word):
        word = json.loads(word)
    speech_singleton.speak(word)
    return json.dumps(asdict(SUCCESS_RES(status=200, success= True)))

@admin_routes.route('/print_to_terminal', methods=['POST'])
def print_to_terminal():
    data = request.json.get('body')
    data_singleton.logger.info(f'/print_to_terminal: {str(data)}')
    print("print_to_terminal: ", data)
    return json.dumps(asdict(SUCCESS_RES(status=200, success= True)))

@admin_routes.route('/publish_command', methods=['POST'])
def publish_command():
    command = request.json.get('command')
    conn_manager.publish_message(Topics.CONTROL, {"command": command})
    # TODO: error handling
    return json.dumps(asdict(SUCCESS_RES(status=200, success= True)))

@admin_routes.route('/publish_select', methods=['POST'])
def publish_select():
    word = request.json.get('word')
    selected = request.json.get('selected')

    conn_manager.publish_message(Topics.word_select(word), {"word": word, "selected": selected})    
    # TODO: return real result
    return json.dumps(asdict(SUCCESS_RES(status=200, success= True)))

@admin_routes.route('/savesession', methods=['POST'])
def save_session():
    data = request.get_json()
    for v,k in data.items():
        session[v] = data[v]
    speech_singleton.clear_queue()
    return json.dumps(asdict(SUCCESS_RES(status=200, success= True)))

@admin_routes.route('/start_game', methods=["POST"])
def start_game(mode: GAME_MODES = None, level: GAME_LEVELS = None):
    data_singleton.mode = mode if mode else request.json.get('mode')
    data_singleton.level = level if level else request.json.get('level')
    conn_manager.publish_message(Topics.CONTROL, {"command": MQTT_COMMANDS.START, "level": data_singleton.level, "mode": data_singleton.mode})
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return json.dumps(asdict(SUCCESS_RES(status=200, success= True)))
    else: return json.dumps(asdict(SUCCESS_RES(status=400, success= False)))
