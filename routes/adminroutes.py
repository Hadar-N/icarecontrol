from flask import request, url_for, Response, stream_with_context, session, Blueprint
import time
import json

from mqtt.MQTTsingle import MQTTSingle
from static.consts import MQTT_COMMANDS

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
        'redirect': url_for('game.game_start') if command == MQTT_COMMANDS.STOP else None
    }
    # TODO: error handling
    return json.dumps(result)

@admin_routes.route('/savesession', methods=['POST'])
def save_session():
    data = request.get_json()
    session['game_status'] = data['status']
    session['matched_list'] = data['matched']
    return json.dumps({"status": "success"})

