import time
import json
from flask import request, url_for, Response, stream_with_context, session, Blueprint, current_app

from mqtt_shared import ConnectionManager, Topics
from game_shared import GAME_STATUS, MQTT_COMMANDS, MQTT_DATA_ACTIONS

from static.consts import COMMAND_TO_STATUS
from utils.speech_single import SpeechSingle
        
admin_routes = Blueprint('adm', __name__)

conn_manager = ConnectionManager.get_instance()
speech_singleton = SpeechSingle()

@admin_routes.route('/speak', methods=['POST'])
def speak():
    word = request.json.get('word')
    speech_singleton.speak(word)
    
    result = {
        'status': 'success',
    }
    return json.dumps(result)

@admin_routes.route('/print_to_terminal', methods=['POST'])
def print_to_terminal():
    data = request.json.get('body')
    print("print_to_terminal: ", data)
    
    result = {
        'status': 'success',
    }
    return json.dumps(result)

@admin_routes.route('/publish_command', methods=['POST'])
def publish_command():
    command = request.json.get('command')
    conn_manager.publish_message(Topics.CONTROL, {"command": command})
    result = {
        'status': 'success',
    }
    
    # TODO: error handling
    return json.dumps(result)

@admin_routes.route('/publish_select', methods=['POST'])
def publish_select():
    word = request.json.get('word')
    selected = request.json.get('selected')

    conn_manager.publish_message(Topics.word_select(word), {"word": word, "selected": selected})
    result = {
        'status': 'success',
    } # TODO: return real result

    return result


@admin_routes.route('/getconstants', methods=['GET'])
def get_consts():
    data = {
        "MQTT_DATA_ACTIONS": {i.name: i.value for i in MQTT_DATA_ACTIONS},
        "GAME_STATUS": {i.name: i.value for i in GAME_STATUS}
    }
    return json.dumps(data)

@admin_routes.route('/savesession', methods=['POST'])
def save_session():
    data = request.get_json()
    for v,k in data.items():
        session[v] = data[v]
    speech_singleton.clear_queue()
    return json.dumps({"status": "success"})
