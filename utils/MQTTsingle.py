import os
import paho.mqtt.client as mqtt
import logging
import json
import threading

from dotenv import load_dotenv
from static.consts import LOGFILE, MQTT_TOPIC_DATA, MQTT_TOPIC_CONTROL, MQTT_COMMANDS

class MQTTSingle:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
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
        self.__last_start_index = 0

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.__on_connect
        self.client.on_publish = self.__on_publish
        self.client.on_message = self.__on_message
        self.client.on_close = self.__on_close
        try:
            self.client.username_pw_set(username=os.getenv("USERNAME"),password=os.getenv("PASSWORD"))
            self.client.connect(os.getenv("HOST"), int(os.getenv("PORT")))
            self.client.loop_start()
            self.__initialized = True
        except Exception as e:
            print("mqtt connection failed! error: ", e)

    def __on_connect(self, client, userdata, flags, rc, props):
        self.__logger.info("Connected with result code "+str(rc))
        print("Connected with result code "+str(rc))
        client.subscribe(MQTT_TOPIC_DATA)

    def __on_close(self):
        self.client.disconnect()
        self.client.loop_stop()

    def __on_publish(self, client, userdata, mid, reason_code, properties):
        try:
            self.__logger.info('message published status: '+ str(reason_code))
            # TODO: error handling
        except KeyError:
            print(KeyError)

    def __on_message(self, client, userdata, msg):
        if msg.topic == MQTT_TOPIC_DATA:
            data = msg.payload.decode()
            self.__messages.append(data)
            self.__logger.info('message received: ' + data)
    
    def publish_control_command(self, command, payload=None):
        msg = json.dumps({
            "command": command,
            "payload": payload
        })
        self.__logger.info(f'publishing to topic: {MQTT_TOPIC_CONTROL} the message: {msg}')
        self.__publish_message(MQTT_TOPIC_CONTROL, msg)
        if command == MQTT_COMMANDS.START.value:
            self.__last_start_index = len(self.__messages)

    def __publish_message(self, topic, msg):
        msg_info = self.client.publish(topic, msg)
        msg_info.wait_for_publish()

    def get_messages(self):
        return self.__messages[self.__last_start_index:]
