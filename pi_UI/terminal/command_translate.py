# encoding=UTF-8

"""
used to translate and execute command line
"""
import terminal.mysql_connect as mysql_connect
import terminal.tools as tools
import paho.mqtt.client as mqtt
import json
import time


class Execute:
    def __init__(self, path):
        """
        all of the command method and their corresponding function need to insert to the
        command list
        :param path: configuration file for host program
        """

        self.__setting = tools.get_server_ini(path)
        self.__mysql_connector = self.__connect_mysql()
        self.__command_list = dict()
        self.__command_list["help"] = self.__help_function
        self.__command_explain = dict()
        self.__terminate_function_list = list()

        self.__command_list["node"] = self.__node_control
        self.__command_explain["node"] = "control NodeMCU"

        self.__command_list["show"] = self.__show_function
        self.__command_explain["show"] = "show data from local mysql database"
        self.__link = 0

    def __node_control(self, args):
        if len(args) == 1:
            print("use node get all（检查全部NodeMCU状态)\n"
                  "    node get number（检查编号为number的NodeMCU状态\n"
                  "    node set number parameter=value parameter=value...\n"
                  "         （设置number编号的NodeMCU的parameter参数的值为value\n"
                  "         parameter:  status: whether start collection, 0 for close collection,"
                  " 1 for start collection\n"
                  "                     mqtt_pub_interview: the interview between collection (ms)\n"
                  "                     wifi_wait_interview: WiFi reconnected interview\n"
                  "                     mqttfinding_wait_interview: MQTT server detect interview\n")
            return True
        if len(args) >= 2:
            if args[1] == "get":
                if len(args) == 2:
                    raise Exception("error in parameter")
                if args[2] == "all":
                    print("@nodemcu")
                    self.__start_mqtt(sleep_time=1, ip="localhost",
                                      publish_name="get_status", payload="all")
                else:
                    self.__start_mqtt(sleep_time=1, ip="localhost",
                                      publish_name="get_status", payload=args[2])
            elif args[1] == "set":
                number = args[2]
                parameter = dict()
                try:
                    for pire in args[3:]:
                        key, value = pire.split("=")
                        parameter[key] = int(value)
                    parameter = json.dumps(parameter)
                    self.__start_mqtt(sleep_time=1, ip="localhost",
                                      publish_name="set_status_" + number,
                                      payload=parameter)
                except:
                    raise Exception("error in parameter")
                pass
            else:
                raise Exception("error in parameter")
        return True

    def __start_mqtt(self, publish_name, payload, ip,  sleep_time=0.05, connect_overtime=1.5):
        client = mqtt.Client()
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message
        self.__mqtt_client = client

        client = self.__mqtt_client
        
        client.connect(ip, 1883, 600)
        client.loop_start()
        self.__mqtt_client.publish(publish_name, payload=payload)
        time.sleep(sleep_time)
        client.loop_stop()
        


    def __on_connect(self, client, userdata, flags, rc):
        self.__mqtt_client.subscribe("node_status")


    def __on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        # message format
        # temp_moist: {"params": {"humi": 10, "temp": 33.5, "name": "nodemcu1"}}
        try:
            message = json.loads(message)
            message = message["params"]
            print(message)
        except:
            pass

    def __connect_mysql(self):
        mysql_connector = mysql_connect.mysql_connector(self.__setting["db_connect_file"])
        try:
            mysql_connector.test_link()
        except Exception as e:
            print("mysql link fail: \"{}\"" + str(e))
            return 0
        return mysql_connector

    def __help_function(self, args):
        print("")
        print("{:<10} {}".format("quit", "quit the progrem"))
        for item in self.__command_list.keys():
            if self.__command_explain.get(item, 0) != 0:
                print("{:<10} {}".format(item, self.__command_explain[item]))
        print()
        return True

    def terminate(self):
        for termimate_function in self.__terminate_function_list:
            try:
                termimate_function()
            except:
                pass

    def execute(self, command):
        command = str(command)
        command = command.strip()
        if command == "":
            return True
        if command == "quit":
            return False
        command = command.split()
        if self.__command_list.get(command[0], 0) == 0:
            raise Exception("\"{}\" is not a valid command".format(command[0]))
        else:
            return self.__command_list[command[0]](command)


    def __show_function(self, args):
        if len(args) == 1:
            print("use show -all          （输出本地数据库全部数据\测试）\n"
                  "use show -num 10       （输出10条数据）\n"
                  "    show -date \"days\"（输出本地数据库全部数据之后的数据\尚未启用）\n")
            return True
        if len(args) == 2 or len(args) == 3:
            if args[1] == "-all":
                data = self.__mysql_connector.select_all()
                tools.show_table(data)
            elif args[1] == "-num":
                try:
                    num = int(args[2])
                except:
                    raise Execute("num type error")
                data = self.__mysql_connector.select_all()
                tools.show_table(data, num)
            return True
        raise Exception("parameter error")
