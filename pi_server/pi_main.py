# encoding=UTF-8
"""
python version: 2.7
essential software: mosquitto
essential libraries for this program are listed as follow:
    pymysql: connect to mysql
    paho: connect to mqtt server
"""

import os
import sys
import subprocess
import io
import tools
from mysql_connect import mysql_connector

# configuration file path for program
server_ini_path = "server.ini"


def main():
    server_ini = tools.get_server_ini(server_ini_path)
    mysql_connect = mysql_connector(server_ini["db_connect_file"])
    test_mysql_link(mysql_connect)
    open_mosquitto_server()
    searching_nodemcu(server_ini_path, server_ini)
    subscribe_mqtt(server_ini_path, server_ini)
    start_tcp_server(server_ini_path, server_ini)


def searching_nodemcu(ini_path, config):
    """
    sending message in the whole range of LAN, demonstrate mqtt server ip address
    :param ini_path: configuration file path for program
    :return: None
    """
    print("starting searching mqtt equipment")
    pi = subprocess.Popen("python searching_equipment.py " + ini_path,
                          # stdin=subprocess.PIPE,
                          # stdout=subprocess.PIPE,
                          # stderr=subprocess.PIPE,
                          shell=True)
    pid = pi.pid
    if not pid:
        print("open subscribe_mqtt.py failed.")
        sys.exit(1)
    save_id("searching_equipment", pid, config["running_state_file"])


def subscribe_mqtt(ini_path, config):
    """
    start mqtt subscribe.
    :param ini_path: configuration file path for program
    :return: None
    """
    print("start mqtt subscribe")
    pi = subprocess.Popen("python subscribe_mqtt.py " + ini_path,
                          # stdin=subprocess.PIPE,
                          # stdout=subprocess.PIPE,
                          # stderr=subprocess.PIPE,
                          shell=True)
    pid = pi.pid
    if not pid:
        print("open subscribe_mqtt.py failed.")
        sys.exit(1)
    save_id("subscribe_mqtt", pid, config["running_state_file"])


def save_id(progress_name, pid, path):
    """
    save progress name and id in a temp file, used to kill each progress when shutdown the progrem.
    :param progress_name:
    :param pid:
    :return: None
    """
    if not os.path.exists(path):
        file = open(path, "w")
        file.close()
    running_state = tools.get_server_ini(str(path))
    running_state[progress_name] = pid
    tools.save_server_int(path, running_state)


def start_tcp_server(ini_path, config):
    print("starting tcp server")
    pi = subprocess.Popen("python tcp_server.py " + ini_path,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True)
    pid = pi.pid
    if not pid:
        print("open subscribe_mqtt.py failed.")
        sys.exit(1)
    save_id("subscribe_mqtt", pid, config["running_state_file"])


def open_mosquitto_server():
    """
    open mosquitto server. Failed to open mosquitto server will exit this program
    :return: None
    """
    print("starting mqtt server")
    subprocess.Popen("python start_mosquitto.py",
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     shell=True)
    pid = get_progress_id("mosquitto")
    if not pid:
        print("mosquitto open failed for unknown reason")
        sys.exit(1)
    else:
        print("mosquitto start successfully, pid: {}".format(pid))


def get_progress_id(name):
    """
    get progress id through progress name
    :param name: progress name
    :return: progress id
    """
    child = subprocess.Popen(["pgrep", "-f", name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0].split()
    return response[-1]


def test_mysql_link(mysql_):
    """
    test for mysql link. Failed for connect mysql will exit the program
    :param mysql_: a mysql_connector object
    :return: None
    """
    print("testing mysql link")
    try:
        mysql_.test_link()
        print("mysql link successful")
    except Exception as e:
        print("mysql link fail：" + str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
