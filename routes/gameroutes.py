import json
from flask import render_template, redirect, url_for, Blueprint, request, after_this_request

from .adminroutes import start_game

from static.consts import FE_CONSTS
from static.fe_strings import STRINGS
from utils.forms import GameStartForm
from utils.curr_data_single import CurrDataSingle
from mqtt_shared import ConnectionManager, Topics
from game_shared import GAME_STATUS, MQTT_COMMANDS

game_routes = Blueprint('game', __name__)
conn_manager = ConnectionManager.get_instance()
data_singleton = CurrDataSingle()

mode_data = STRINGS["gamestart.html"]["mode"]
level_data = STRINGS["gamestart.html"]["level"]

@game_routes.route('/game/', methods=['GET', 'POST'])
def game_start():
    form = GameStartForm()
    if not (form.mode.data and form.mode.data in mode_data["options"]) and data_singleton.mode:
        form.mode.data = data_singleton.mode

    if form.validate_on_submit():
        start_game(form.mode.data, form.level.data)
    
    return pack_render_temp('gamestart.html', form=form)

@game_routes.route('/game/process')
def game_process():
    level = data_singleton.level
    mode = data_singleton.mode

    if (not level or level not in level_data["options"]) or (not mode or mode not in mode_data["options"]):
        # TODO: status check
        print('Invalid game properties. Please select mode and level.')
        return redirect(url_for('game.game_start'))
        
    return pack_render_temp('gameprocess.html')

@game_routes.route('/game/end', methods=['GET'])
def game_end():
    status = data_singleton.status
    matched = data_singleton.matched_words

    if not status or status not in [l.value for l in GAME_STATUS]:
        print('Invalid data. Please start game.', status, matched)
        return redirect(url_for('game.game_start'))
    
    @after_this_request
    def refresh_gamestats(res):
        data_singleton.restart_config()
        return res

    return pack_render_temp('gameend.html', status=status, matched=matched)

def pack_render_temp(url: str, **kwargs):
    return render_template(url, constants=FE_CONSTS, strings=STRINGS,
                           level=data_singleton.level, mode=data_singleton.mode,
                           **kwargs)