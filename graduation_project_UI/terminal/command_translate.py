# encoding=UTF-8

"""
used to translate and execute command line
"""
import terminal.mysql_connect as mysql_connect
import terminal.tools as tools
import terminal.link as link
import paho.mqtt.client as mqtt
import json
import time
from threading import Thread


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

        self.__command_list["link"] = self.__link_mqtt
        self.__command_explain["link"] = "connect to remote raspberry pi service"
        self.__terminate_function_list.append(self.__close_link)
        self.__command_list["db"] = self.__mysql_mqtt
        self.__command_explain["db"] = "mysql operation"

        self.__command_list["node"] = self.__node_control
        self.__command_explain["node"] = "control NodeMCU"

        self.__command_list["get"] = self.__get_function
        self.__command_explain["get"] = "transmit data from remote raspberry pi service"
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
                    self.__start_mqtt(sleep_time=1, ip="192.168.31.67",
                                      publish_name="get_status", payload="all")
                else:
                    self.__start_mqtt(sleep_time=1, ip="192.168.31.67",
                                      publish_name="get_status", payload=args[2])
            elif args[1] == "set":
                number = args[2]
                parameter = dict()
                try:
                    for pire in args[3:]:
                        key, value = pire.split("=")
                        parameter[key] = int(value)
                    parameter = json.dumps(parameter)
                    self.__start_mqtt(sleep_time=1, ip="192.168.31.67",
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
        """
        client.connect(ip, 1883, 600)
        client.loop_start()
        self.__mqtt_client.publish(publish_name, payload=payload)
        time.sleep(sleep_time)
        client.loop_stop()

        """
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
        """
        client.publish('get_status', payload='all')

        du = {"status": 0, "mqtt_pub_interview": 5000}
        a = json.dumps(du)
        client.publish('set_status_00101', payload=a)
        """

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

    def __mysql_mqtt(self, args):
        if len(args) == 1:
            print("use db -state（检查mqtt连接状态)")
            return True
        if len(args) == 2:
            if args[1] == "-state":
                if self.__mysql_connector == 0:
                    print("mysql not connect")
                else:
                    print("mysql connect successfully")
            return True

        raise Exception("parameter error")

    def __close_link(self):
        try:
            self.__link.close_tcp()
        except:
            pass

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

    def __link_mqtt(self, args):
        if len(args) == 1:
            print("use link -state（检查mqtt连接状态）\n"
                  "    link -start（开始连接）\n"
                  "    link -close（关闭连接）\n")
            return True
        if len(args) != 2:
            raise Exception("link syntax error")
        command = args[1].strip()
        if command == "-state":
            if self.__link != 0:
                if self.__link.get_link_state() == 1:
                    mqtt_ip = self.__link.get_mqtt_ip()
                    print("mqtt server ip: {}\n".format(mqtt_ip))
                elif self.__link.get_searching_state() == 1:
                    print("searcing mqtt service")
                else:
                    print("mqtt server is not on line, searching is not start")
            else:
                print("mqtt server is not on line, searching is not start")
            return True

        if command == "-start":
            print("start linking mqtt")
            if self.__link == 0:
                self.__link = link.Link(int(self.__setting["search_time"]),
                                        self.__setting["mqtt_port"],
                                        int(self.__setting["tcp_port"]),
                                        self.__setting["mqtt_content"],
                                        int(self.__setting["tcp_timeout"]),
                                        int(self.__setting["tcp_keep_port"]))
            selfip = self.__link.get_windows_ip()
            if selfip == 0:
                raise Exception("ip read filed")
            self.__link.open_listen(selfip)
            self.__link.start_searching(selfip)

            return True

        if command == "-close":
            try:
                self.__link.close_tcp()
                self.__link = 0
            except:
                pass
            return True
        raise Exception("parameter error")

    def __get_function(self, args):
        if len(args) == 1:
            print("use get -all           （获取mqtt服务器全部数据\测试）\n"
                  "    get -update        （更新mqtt尚未发送的数据\尚未启用）\n"
                  "    get -date \"days\" （获取指定天数之后的数据\尚未启用）\n")
            return True
        if len(args) == 2:
            if args[1] == "-all":
                if self.__link == 0:
                    raise Exception("mqtt link is not established")
                if self.__link.get_link_state == 0:
                    raise Exception("mqtt link is not established")
                data = self.__link.tcp_communication("get -all", set_time_out=True)
                try:
                    data = eval(data)
                except:
                    return True
                tools.show_table(data)
                print("data transmit successfully")

                self.__mysql_connector.insert_localhost_with_check(data)
                print("data write to mysql successfully")
                return True
        raise Exception("parameter error")

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
