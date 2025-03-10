from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, ValidationError

from static.consts import GAME_LEVELS, GAME_OPTIONS

def ValidateLevel(form, field):
    if not (field.data and field.data in [l.value for l in GAME_LEVELS]):
        raise ValidationError("Please select a game level")

def ValidateOption(form, field):
    print(field.data)
    if not (field.data and field.data in [l.value for l in GAME_OPTIONS]):
        raise ValidationError("Please select a game option")

class GameStartForm(FlaskForm):
    option = RadioField('Game Options:', 
        choices=[(opt.name, opt.value) for opt in GAME_OPTIONS],
        validators=[ValidateOption],
    )
    level = RadioField('Choose a Level:', 
        choices=[(level.value, level.value) for level in GAME_LEVELS],
        validators=[ValidateLevel],
    )