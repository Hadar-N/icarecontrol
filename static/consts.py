from enum import Enum

LOGFILE= "running.log"

class GAME_LEVELS(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

MQTT_TOPIC_CONTROL = "game/control"
MQTT_TOPIC_DATA = "game/data"
class MQTT_COMMANDS(str, Enum):
    START = "start"
    PAUSE = "pause"
    STOP = "stop"
