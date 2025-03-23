from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, ValidationError

from static.fe_strings import STRINGS

level_data = STRINGS["gamestart.html"]["level"]
mode_data = STRINGS["gamestart.html"]["mode"]

def ValidateLevel(form, field):
    if not (field.data and field.data in level_data["options"]):
        raise ValidationError(level_data["err_msg"])

def ValidateMode(form, field):
    if not (field.data and field.data in mode_data["options"]):
        raise ValidationError(mode_data["err_msg"])

class GameStartForm(FlaskForm):
    mode = RadioField(mode_data["title"], 
        choices=[(v[0], v[1]) for v in mode_data["options"].items()],
        validators=[ValidateMode],
    )
    level = RadioField(level_data["title"], 
        choices=[(v[0], v[1]) for v in level_data["options"].items()],
        validators=[ValidateLevel],
    )