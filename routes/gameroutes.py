import json
from flask import render_template, redirect, url_for, session, Blueprint

from utils.MQTTsingle import MQTTSingle
from static.consts import MQTT_COMMANDS, GAME_LEVELS, GAME_OPTIONS, GAME_STATUS, JS_CONSTANTS
from utils.forms import GameStartForm

game_routes = Blueprint('game', __name__)
mqtt_singleton = MQTTSingle()

@game_routes.route('/game/', methods=['GET', 'POST'])
def game_start():
    form = GameStartForm()
    stage_1_choice = form.option.data if form.option.data in [l.name for l in GAME_OPTIONS] else ''

    if form.validate_on_submit():
        session['game_level'] = form.level.data
        session['game_option'] = stage_1_choice
        return redirect(url_for('game.game_process'))
    
    return render_template('gamestart.html', form=form, stage_1_choice=stage_1_choice)

@game_routes.route('/game/process')
def game_process():
    level = session.get('game_level')
    option = session.get('game_option')

    if (not level or level not in [l.value for l in GAME_LEVELS]) or (not option or option not in [l.name for l in GAME_OPTIONS]):
        # TODO: status check
        print('Invalid game properties. Please select option and level.')
        return redirect(url_for('game.game_start'))
    
    session.pop('game_level', None)
    
    mqtt_singleton.publish_control_command(MQTT_COMMANDS.START, {"level": level, "option": option})
    return render_template('gameprocess.html', level=level, btns=MQTT_COMMANDS, constants=JS_CONSTANTS)

@game_routes.route('/game/end', methods=['GET'])
def game_end():
    status = session.get('game_status')
    matched = session.get('matched_list', [])

    if not status or status not in [l.value for l in GAME_STATUS]:
        print('Invalid data. Please start game.')
        return redirect(url_for('game.game_start'))

    session.pop('game_status', None)
    session.pop('matched_list', None)

    return render_template('gameend.html', status=status, matched=matched, constants=JS_CONSTANTS)