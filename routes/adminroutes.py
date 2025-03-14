import time
import json
from flask import request, url_for, Response, stream_with_context, session, Blueprint

from static.consts import COMMAND_TO_STATUS, LOGFILE, MQTT_TOPIC_CONTROL
from mqtt_shared import ConnectionManager, Topics, BodyForTopic
from game_shared import GAME_STATUS, MQTT_COMMANDS
from utils.speechSingle import SpeechSingle
        
admin_routes = Blueprint('adm', __name__)

conn_manager = ConnectionManager.get_instance()
speech_singleton = SpeechSingle()

@admin_routes.route('/stream')
def stream():
    def generate():
        message_count = 0
        while True:
            current_messages = conn_manager.get_words()
            if len(current_messages) > message_count:
                new_messages = current_messages[message_count:]
                message_count = len(current_messages)
                yield f"data: {json.dumps(new_messages)}\n\n"
            time.sleep(1)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@admin_routes.route('/speak', methods=['POST'])
def speak():
    word = request.json.get('word')
    speech_singleton.speak(word)
    
    result = {
        'status': 'success',
    }
    return json.dumps(result)

@admin_routes.route('/publish', methods=['POST'])
def publish():
    command = request.json.get('command')
    conn_manager.publish_message(Topics.CONTROL, BodyForTopic(Topics.CONTROL, {"command": command}))
    result = {
        'status': 'success',
    }
    if command == MQTT_COMMANDS.STOP:
        mlist = request.json.get('matched')
        save_to_session(COMMAND_TO_STATUS[command].value, mlist)
        result["redirect"] = url_for('game.game_end')
    
    # TODO: error handling
    return json.dumps(result)

@admin_routes.route('/savesession', methods=['POST'])
def save_session():
    data = request.get_json()
    save_to_session(data['status'], data['matched'])
    speech_singleton.clear_queue()
    return json.dumps({"status": "success"})

def save_to_session(status, matched_list):
    session['game_status'] = status
    session['matched_list'] = matched_list
