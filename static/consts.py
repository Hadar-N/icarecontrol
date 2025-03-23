from enum import Enum
from game_shared import GAME_STATUS, MQTT_COMMANDS, MQTT_DATA_ACTIONS

LOGFILE= "running.log"

# mqtt consts
class WEB_ACTIONS(str, Enum):
    START = MQTT_COMMANDS.START.value
    PAUSE = MQTT_COMMANDS.PAUSE.value
    STOP = MQTT_COMMANDS.STOP.value

COMMAND_TO_STATUS= {
    MQTT_COMMANDS.START: GAME_STATUS.ACTIVE,
    MQTT_COMMANDS.PAUSE: GAME_STATUS.HALTED,
    MQTT_COMMANDS.STOP: GAME_STATUS.HALTED
}

FE_CONSTS = {
    "MQTT_DATA_ACTIONS": {i.name: i.value for i in MQTT_DATA_ACTIONS},
    "GAME_STATUS": {i.name: i.value for i in GAME_STATUS}
}