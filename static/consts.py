from enum import Enum
from game_shared import GAME_STATUS, MQTT_COMMANDS

LOGFILE= "running.log"

class GAME_MODES(str, Enum):
    ENtoZH = '英↓中'
    ZHtoEN = '中↓英'
class GAME_LEVELS(str, Enum):
    BEGINNER = "低年"
    INTERMEDIATE = "中年"
    ADVANCED = "高年"

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