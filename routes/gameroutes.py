import json
from flask import render_template, redirect, url_for, session, Blueprint

from static.consts import GAME_LEVELS, GAME_MODES, WEB_ACTIONS
from utils.forms import GameStartForm
from mqtt_shared import ConnectionManager, Topics
from game_shared import GAME_STATUS, MQTT_COMMANDS

game_routes = Blueprint('game', __name__)
conn_manager = ConnectionManager.get_instance()

@game_routes.route('/game/', methods=['GET', 'POST'])
def game_start():
    form = GameStartForm()
    stage_1_choice = form.mode.data if form.mode.data in [l.name for l in GAME_MODES] else ''

    if form.validate_on_submit():
        session['game_level'] = form.level.data
        session['game_mode'] = stage_1_choice
        return redirect(url_for('game.game_process'))
    
    return render_template('gamestart.html', form=form, stage_1_choice=stage_1_choice)

@game_routes.route('/game/process')
def game_process():
    level = session.get('game_level')
    mode = session.get('game_mode')

    if (not level or level not in [l.name for l in GAME_LEVELS]) or (not mode or mode not in [l.name for l in GAME_MODES]):
        # TODO: status check
        print('Invalid game properties. Please select mode and level.')
        return redirect(url_for('game.game_start'))
    
    session.pop('game_level', None)
    
    conn_manager.publish_message(Topics.CONTROL, {"command": MQTT_COMMANDS.START, "level": level, "mode": mode})
    return render_template('gameprocess.html', level=level, btns=WEB_ACTIONS)

@game_routes.route('/game/end', methods=['GET'])
def game_end():
    status = session.get('game_status')
    matched = session.get('matched_list', [])

    if not status or status not in [l.value for l in GAME_STATUS]:
        print('Invalid data. Please start game.', status, matched)
        return redirect(url_for('game.game_start'))

    session.pop('game_status', None)
    session.pop('matched_list', None)

    return render_template('gameend.html', status=status, matched=matched)