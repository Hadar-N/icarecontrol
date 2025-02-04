from flask_wtf import FlaskForm
from wtforms import SelectField, ValidationError

from static.consts import GAME_LEVELS

def ValidateLevel(form, field):
    if not (field.data and field.data in [l.value for l in GAME_LEVELS]):
        raise ValidationError("Please select a game level")

class GameStartForm(FlaskForm):
    level = SelectField('Choose a level:', 
        choices=[('','')] + [(level.value, level.name.title()) for level in GAME_LEVELS],
        validators=[ValidateLevel]
    )