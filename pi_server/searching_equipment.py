# encoding=UTF-8
"""
sending udp message to activate nodemcu equipment
"""

import socket
import time
import os
import sys
import tools


def main():
    lan_ip = tools.find_lan_ip_address()
    if lan_ip == 0:
        print("error happened in searching lan ip address")
        sys.exit()
    start_searching(lan_ip)


def start_searching(lan_ip):
    lan_base = lan_ip.rsplit(".", 1)[0] + "."
    server_ini = tools.get_server_ini(sys.argv[1])
    mqtt_searching_frequent = int(server_ini["mqtt_searching_frequent"])
    mqtt_searching_port = int(server_ini["mqtt_searching_port"])
    mqtt_confirm_message = server_ini["mqtt_confirm_message"]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        for iptemp in range(1, 254):
            ip = lan_base + str(iptemp)
            msg = str(mqtt_confirm_message).encode()
            server_address = (ip, mqtt_searching_port)
            client_socket.sendto(msg, server_address)
        time.sleep(mqtt_searching_frequent)


if __name__ == "__main__":
    main()
