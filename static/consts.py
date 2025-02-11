from enum import Enum

LOGFILE= "running.log"

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
class MQTT_STATUSES(str,Enum):
    ONGOING = "ongoing"
    FINISHED = "finished"
    STOPPED = "stopped"
    ERROR = "error"
class MQTT_COMMANDS(str, Enum):
    START = "start"
    PAUSE = "pause"
    STOP = "stop"

JS_CONSTANTS = {
    "MQTT_DATA_ACTIONS": {i.name: i.value for i in MQTT_DATA_ACTIONS},
    "MQTT_STATUSES": {i.name: i.value for i in MQTT_STATUSES}
}