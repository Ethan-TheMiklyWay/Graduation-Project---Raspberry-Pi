import paho.mqtt.client as mqtt
import json
import time
from threading import Thread

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect_async("192.168.31.67", 1883, 600)

    time.sleep(1)
    print(client.is_connected())

    client.loop_start()
    # print(client.is_connected())
    time.sleep(1)
    client.publish('get_status', payload='all')


    time.sleep(1)

    client.loop_stop()
    #client.loop_forever()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))
    client.subscribe("node_status")
    #client.publish('get_status', payload='all')

    """
    du = {"status": 0, "mqtt_pub_interview": 7000}
    a = json.dumps(du)
    client.publish('set_status_00102', payload=a)
    """


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    # message format
    # temp_moist: {"params": {"humi": 10, "temp": 33.5, "name": "nodemcu1"}}
    print(message)


if __name__ == "__main__":
    main()
