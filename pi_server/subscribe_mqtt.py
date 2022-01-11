# encoding=UTF-8
"""
subscribe mqtt service:
    1. start subscription
    2. open a upd server, listen for nodemcu connect
    3. give
"""
import tools
import sys
import paho.mqtt.client as mqtt
from mysql_connect import mysql_connector
import time

subscribe_content = ""
pi_id = ""
min_record_time = 1000
nodemcu_id_recordtime = {}
mysql_connect = None


def main():
    global mysql_connect, pi_id
    server_ini = tools.get_server_ini(sys.argv[1])
    pi_id = server_ini["pi_id"]
    mysql_connect = mysql_connector(server_ini["db_connect_file"])
    start_subscribe(server_ini)


def start_subscribe(server_ini):
    global subscribe_content, min_record_time
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    subscribe_content = server_ini["mqtt_sub_name"]
    mqtt_server_ip = server_ini["mqtt_server_address"]
    mqtt_port = int(server_ini["mqtt_port"])
    mqtt_timeout = int(server_ini["mqtt_timeout"])
    min_record_time = int(server_ini["mqtt_min_record"])
    client.connect(mqtt_server_ip, mqtt_port, mqtt_timeout)
    client.loop_forever()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}, subscribe content: {}".format(rc, subscribe_content))
    client.subscribe(subscribe_content)


def on_message(client, userdata, msg):
    # judge
    # insert into db
    # auto connect mqtt server

    global nodemcu_id_recordtime
    message = msg.payload.decode()
    # message format
    # temp_moist: {"params": {"humi": 10, "temp": 33.5, "name": "nodemcu1"}}
    try:
        message = eval(message.split(":", 1)[-1][0:-1])
    except:
        print("format error in mqtt return")
        sys.exit(1)

    nodemcu_name = message["name"]
    time_record = nodemcu_id_recordtime.get(nodemcu_name, 0)
    if time_record == 0:
        nodemcu_id_recordtime[nodemcu_name] = time.time()
        insert_to_mysql(message)
    elif time.time() - time_record > min_record_time:
        nodemcu_id_recordtime[nodemcu_name] = time.time()
        insert_to_mysql(message)
    else:
        pass


def insert_to_mysql(message):
    content = {
        "pi_id": pi_id,
        "nodemcu_id": message["name"],
        "temperature": float(message["temp"]),
        "moisture": float(message["humi"])
    }
    mysql_connect.insert(content)
    pass


if __name__ == "__main__":
    main()
