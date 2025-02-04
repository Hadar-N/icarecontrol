import os
import paho.mqtt.client as mqtt
import logging
from dotenv import load_dotenv
from static.consts import LOGFILE

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

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
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

    def on_close(self):
        self.client.disconnect()
        self.client.loop_stop()

    def on_publish(self, client, userdata, mid, reason_code, properties):
        try:
            self.__logger.info('message published status: '+ str(reason_code))
        except KeyError:
            print(KeyError)

    def publish_message(self,TOPIC, msg):
        msg_info = self.client.publish(TOPIC, msg)
        msg_info.wait_for_publish()