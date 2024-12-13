import os
from dotenv import load_dotenv
from mqtt.pub import *

load_dotenv(verbose=True, override=True)
TOPIC = os.getenv("TOPIC")

mqttc = connect_func()

publish_message(mqttc, TOPIC, 123)
publish_message(mqttc, TOPIC, "abc")
publish_message(mqttc, TOPIC, "last attempt")

disconnect_func(mqttc)