from enum import Enum
from game_shared import GAME_STATUS, MQTT_COMMANDS

LOGFILE= "running.log"

class GAME_MODES(str, Enum):
    ENtoZH = '英↓中'
    ZHtoEN = '中↓英'
class GAME_LEVELS(str, Enum):
    BEGINNER = "4th grade"
    INTERMEDIATE = "5th grade"
    ADVANCED = "6th grade"

# mqtt consts
MQTT_TOPIC_CONTROL = "game/control"
MQTT_TOPIC_DATA = "game/data"
class WEB_ACTIONS(str, Enum):
    START = MQTT_COMMANDS.START.value
    PAUSE = MQTT_COMMANDS.PAUSE.value
    STOP = MQTT_COMMANDS.STOP.value

COMMAND_TO_STATUS= {
    MQTT_COMMANDS.START: GAME_STATUS.ACTIVE,
    MQTT_COMMANDS.PAUSE: GAME_STATUS.HALTED,
    MQTT_COMMANDS.STOP: GAME_STATUS.HALTED
}