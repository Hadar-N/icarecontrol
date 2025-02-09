from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, ValidationError

from static.consts import GAME_LEVELS

def ValidateLevel(form, field):
    if not (field.data and field.data in [l.value for l in GAME_LEVELS]):
        raise ValidationError("Please select a game level")

class GameStartForm(FlaskForm):
    level = RadioField('Choose a Level:', 
        choices=[(level.value, level.value) for level in GAME_LEVELS],
        validators=[ValidateLevel],
    )