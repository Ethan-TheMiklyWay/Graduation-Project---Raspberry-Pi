from command.command_base.command_base import CommandBase
import paho.mqtt.client as mqtt
import time
import json


class NodeCommand(CommandBase):
    def __init__(self):
        pass

    def execute(self, args):
        if len(args) == 2:
            if args[0] == "get":
                if args[1] == "all":
                    return self.__get_all_command(ip="192.168.31.67")
                else:
                    return "parameter error"
            elif args[0] == "set":
                return self.__set_command(args[1:], ip="192.168.31.67")
            else:
                return "parameter error"
        else:
            return "parameter error"


    get_all_command_return = []

    def __get_all_command(self, ip):
        NodeCommand.get_all_command_return = []
        self.__start_mqtt(sleep_time=1, ip=ip,
                          publish_name="get_status", payload="all")
        return str(NodeCommand.get_all_command_return)

    def __set_command(self, args, ip):
        number = args[0]
        parameter = dict()
        try:
            for pire in args[1:]:
                key, value = pire.split("=")
                parameter[key] = int(value)
            parameter = json.dumps(parameter)
            self.__start_mqtt(sleep_time=1, ip=ip,
                              publish_name="set_status_" + number,
                              payload=parameter)
            return "success"
        except:
            raise Exception("error in parameter")

    def __start_mqtt(self, publish_name, payload, ip, sleep_time=0.5, connect_overtime=0.5):
        client = mqtt.Client()
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message
        self.__mqtt_client = client

        client.connect_async(ip, 1883, 600)
        client.loop_start()
        time.sleep(connect_overtime)
        if not client.is_connected():
            client.disconnect()
            raise Exception("mqtt server connect overtime")
        else:
            self.__mqtt_client.publish(publish_name, payload=payload)
            time.sleep(sleep_time)
            client.loop_stop()

    def __on_connect(self, client, userdata, flags, rc):
        self.__mqtt_client.subscribe("node_status")

    def __on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        try:
            message = json.loads(message)
            message = message["params"]
            NodeCommand.get_all_command_return.append(message)
        except:
            pass
