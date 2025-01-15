from flask import Flask, request, render_template
from mqtt.MQTTsingle import MQTTSingle
from static.consts import MQTT_TOPIC_CONTROL, MQTT_COMMANDS

app = Flask(__name__)
mqtt_singleton = MQTTSingle()

@app.route('/')
def index(errormsg = ""):
    return render_template('gamestart.html', errormsg=errormsg)

@app.route('/game/<action>', methods=['POST'])
def game_action(action):
    level = request.form.get('level')
    if level:
        mqtt_singleton.publish_message(MQTT_TOPIC_CONTROL, MQTT_COMMANDS.START)
        return render_template('gameprocess.html')
    else: 
        return index("field is mandatory")

if __name__ == '__main__':
    app.run()