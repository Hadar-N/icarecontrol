import os
import paho.mqtt.client as mqtt
import logging

from dotenv import load_dotenv
from static.consts import LOGFILE, MQTT_TOPIC_DATA, MQTT_TOPIC_CONTROL

class MQTTSingle:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MQTTSingle, cls).__new__(cls)
            cls.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        
        load_dotenv(verbose=True, override=True)

        logging.basicConfig(filename=LOGFILE)
        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.DEBUG)

        self.__messages = []

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        try:
            self.client.username_pw_set(username=os.getenv("USERNAME"),password=os.getenv("PASSWORD"))
            self.client.connect(os.getenv("HOST"), int(os.getenv("PORT")))
            self.client.loop_start()
            self.__initialized = True
        except Exception as e:
            print("mqtt connection failed! error: ", e)

    def on_connect(self, client, userdata, flags, rc, props):
        self.__logger.info("Connected with result code "+str(rc))
        print("Connected with result code "+str(rc))
        client.subscribe(MQTT_TOPIC_DATA)

    def on_close(self):
        self.client.disconnect()
        self.client.loop_stop()

    def on_publish(self, client, userdata, mid, reason_code, properties):
        try:
            self.__logger.info('message published status: '+ str(reason_code))
            # TODO: error handling
        except KeyError:
            print(KeyError)

    def on_message(self, client, userdata, msg):
        if msg.topic == MQTT_TOPIC_DATA:
            data = msg.payload.decode()
            self.__messages.append(data)
            # TODO: move word/finish distinguishment here?
    
    def publish_message(self, msg):
        msg_info = self.client.publish(MQTT_TOPIC_CONTROL, msg)
        msg_info.wait_for_publish()

    def get_messages(self):
        return self.__messages
