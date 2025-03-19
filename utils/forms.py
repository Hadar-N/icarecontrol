from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, ValidationError

from static.consts import GAME_LEVELS, GAME_MODES

def ValidateLevel(form, field):
    if not (field.data and field.data in [l.name for l in GAME_LEVELS]):
        raise ValidationError("Please select a game level")

def ValidateMode(form, field):
    if not (field.data and field.data in [l.name for l in GAME_MODES]):
        raise ValidationError("Please select a game mode")

class GameStartForm(FlaskForm):
    mode = RadioField('Game Modes:', 
        choices=[(opt.name, opt.value) for opt in GAME_MODES],
        validators=[ValidateMode],
    )
    level = RadioField('Choose a Level:', 
        choices=[(level.name, level.value) for level in GAME_LEVELS],
        validators=[ValidateLevel],
    )