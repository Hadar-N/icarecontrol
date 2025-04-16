import time
import json
from flask import request, session, Blueprint

from mqtt_shared import ConnectionManager, Topics

from utils.speech_single import SpeechSingle
        
admin_routes = Blueprint('adm', __name__)

conn_manager = ConnectionManager.get_instance()
speech_singleton = SpeechSingle()

@admin_routes.route('/speak', methods=['POST'])
def speak():
    word = request.json.get('word')
    speech_singleton.speak(f'{word} .')
    
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
    }
    
    # TODO: return real result
    return json.dumps(result)

@admin_routes.route('/savesession', methods=['POST'])
def save_session():
    data = request.get_json()
    for v,k in data.items():
        session[v] = data[v]
    speech_singleton.clear_queue()
    return json.dumps({"status": "success"})
