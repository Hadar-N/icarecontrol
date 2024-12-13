# PUBLISHER EXAMPLE
import os
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

def on_publish(client, userdata, mid, reason_code, properties):
    # reason_code and properties will only be present in MQTTv5. It's always unset in MQTTv3
    try:
        print("cannot remove userdata since there is none", mid)
        # userdata.remove(mid)
    except KeyError:
        print(KeyError)

def publish_message(mqttc,TOPIC, msg):
    # Our application produce some messages
    msg_info = mqttc.publish(TOPIC, msg)
    # unacked_publish.add(msg_info.mid)

    # Due to race-condition described above, the following way to wait for all publish is safer
    msg_info.wait_for_publish()

def connect_func() :
    load_dotenv(verbose=True, override=True)

    print("AAAA", os.getenv("USERNAME"))
    # unacked_publish = set()
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_publish = on_publish

    # mqttc.user_data_set(unacked_publish)
    mqttc.username_pw_set(username=os.getenv("USERNAME"),password=os.getenv("PASSWORD"))
    mqttc.connect(os.getenv("HOST"), int(os.getenv("PORT")))
    mqttc.loop_start()

    print("BBBB", os.getenv("HOST"))
    return mqttc

def disconnect_func(mqttc):
    mqttc.disconnect()
    mqttc.loop_stop()
