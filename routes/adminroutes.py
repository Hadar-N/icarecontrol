from flask import request, url_for, Response, stream_with_context, session, Blueprint
import time
import json

from utils.MQTTsingle import MQTTSingle
from static.consts import MQTT_COMMANDS, COMMAND_TO_STATUS

admin_routes = Blueprint('adm', __name__)
mqtt_singleton = MQTTSingle()

@admin_routes.route('/stream')
def stream():
    def generate():
        message_count = 0
        while True:
            current_messages = mqtt_singleton.get_messages()
            if len(current_messages) > message_count:
                new_messages = current_messages[message_count:]
                message_count = len(current_messages)
                yield f"data: {json.dumps(new_messages)}\n\n"
            time.sleep(1)

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@admin_routes.route('/publish', methods=['POST'])
def publish():
    command = request.json.get('command')
    mqtt_singleton.publish_control_command(command)
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
    return json.dumps({"status": "success"})

def save_to_session(status, matched_list):
    session['game_status'] = status
    session['matched_list'] = matched_list
