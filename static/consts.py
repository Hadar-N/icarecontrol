from enum import Enum

LOGFILE= "running.log"

class GAME_OPTIONS(str, Enum):
    ENtoZH = '英↓中'
    ZHtoEN = '中↓英'
class GAME_LEVELS(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

# mqtt consts
MQTT_TOPIC_CONTROL = "game/control"
MQTT_TOPIC_DATA = "game/data"
class MQTT_DATA_ACTIONS(str,Enum):
    NEW = "new"
    REMOVE = "remove"
    MATCHED = "matched"
    STATUS = "status"
class GAME_STATUS(str, Enum):
    ACTIVE= "active"
    HALTED= "halted"
    DONE= "done"
class MQTT_COMMANDS(str, Enum):
    START = "start"
    PAUSE = "pause"
    STOP = "stop"
# COMMAND_TO_STATUS= {
#     MQTT_COMMANDS.START: MQTT_STATUSES.ONGOING,
#     MQTT_COMMANDS.PAUSE: MQTT_STATUSES.PAUSED,
#     MQTT_COMMANDS.STOP: MQTT_STATUSES.STOPPED
# }
COMMAND_TO_STATUS= {
    MQTT_COMMANDS.START: GAME_STATUS.ACTIVE,
    MQTT_COMMANDS.PAUSE: GAME_STATUS.HALTED,
    MQTT_COMMANDS.STOP: GAME_STATUS.HALTED
}

JS_CONSTANTS = {
    "MQTT_DATA_ACTIONS": {i.name: i.value for i in MQTT_DATA_ACTIONS},
    "GAME_STATUS": {i.name: i.value for i in GAME_STATUS}
}