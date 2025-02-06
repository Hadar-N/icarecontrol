import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, session, Response, stream_with_context
import time
import json

from mqtt.MQTTsingle import MQTTSingle
from static.consts import MQTT_TOPIC_CONTROL, MQTT_COMMANDS, GAME_LEVELS
from utils.forms import GameStartForm

load_dotenv(verbose=True, override=True)

app = Flask(__name__)
mqtt_singleton = MQTTSingle()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

@app.route('/', methods=['GET', 'POST'])
def game_start():
    form = GameStartForm()
    
    if form.validate_on_submit():
        session['game_level'] = form.level.data
        return redirect(url_for('game_process'))
    
    return render_template('gamestart.html', form=form)

@app.route('/gameprocess')
def game_process():
    level = session.get('game_level')

    if not level or level not in [l.value for l in GAME_LEVELS]:
        # TODO: status check
        print('Invalid game level. Please select a level.')
        return redirect(url_for('game_start'))
    
    session.pop('game_level', None)
    
    mqtt_singleton.publish_message(MQTT_COMMANDS.START)
    return render_template('gameprocess.html', level=level, btns=MQTT_COMMANDS)

@app.route('/stream')
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

@app.route('/publish', methods=['POST'])
def publish():
    command = request.json.get('command')
    mqtt_singleton.publish_message(command)
    # TODO: error handling
    return json.dumps({'status': 'success'})

if __name__ == '__main__':
    app.run()