from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, ValidationError

from static.fe_strings import STRINGS

gamestart_strings = STRINGS["gamestart.html"]

def ValidateLevel(form, field):
    if not (field.data and field.data in gamestart_strings["level"]["options"]):
        raise ValidationError(gamestart_strings["level"]["err_msg"])

def ValidateMode(form, field):
    if not (field.data and field.data in gamestart_strings["mode"]["options"]):
        raise ValidationError(gamestart_strings["mode"]["err_msg"])

class GameStartForm(FlaskForm):
    mode = RadioField(gamestart_strings["mode"]["title"], 
        choices=[(v[0], v[1]) for v in gamestart_strings["mode"]["options"].items()],
        validators=[ValidateMode],
    )
    level = RadioField(gamestart_strings["level"]["title"], 
        choices=[(v[0], v[1]) for v in gamestart_strings["level"]["options"].items()],
        validators=[ValidateLevel],
    )

    def getStages(self):
        return [{
            "type": "non-active",
            "name": "home",
            "reference": gamestart_strings["home"]
        },
        {
            "type": "radio",
            "name": "mode",
            "reference": self.mode
        },
        {
            "type": "radio",
            "name": "level",
            "reference": self.level
        }]