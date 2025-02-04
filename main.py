import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, session

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
    
    mqtt_singleton.publish_message(MQTT_TOPIC_CONTROL, MQTT_COMMANDS.START)
    return render_template('gameprocess.html', level=level)

if __name__ == '__main__':
    app.run()