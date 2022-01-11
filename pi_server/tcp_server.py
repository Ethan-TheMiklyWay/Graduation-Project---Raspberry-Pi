# encoding=UTF-8
""""
used to connect data to the host
"""
import tools
import sys
import socket
import struct
import mysql_connect
import threading
import time
command_list = dict()
tcp = 0
tcp_keep_alive = 0
mysql_connector = 0

def main():
    # start listen port 5001, udp
    # when connect, get ip, start tcp connect, close udp port.
    # process information
    # when finish, start udp listen
    global command_list,mysql_connector
    command_list["get"] = get_function
    server_ini = tools.get_server_ini(sys.argv[1])
    print(server_ini["db_connect_file"])
    mysql_connector = mysql_connect.mysql_connector(server_ini["db_connect_file"])
    while True:
        client_ip = start_listen(server_ini["waiting_port"], server_ini["waiting_message"])
        start_tcp(client_ip, int(server_ini["tcp_port"]), int(server_ini["tcp_alive_port"]))


def get_function(args):
    if tcp == 0:
        raise Exception("tcp is not online")
    if len(args) == 2:
        
        if args[1] == "-all":
            data = mysql_connector.select_all()
            return_data = []
            for row in data:
                return_data.append(list(row))
            return str(return_data) #str(mysql_connector.select_all())


def start_tcp(tcp_ip, tcp_port, alive_port):
    global tcp
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp.connect((tcp_ip, tcp_port))
        alive = threading.Thread(target=keep_alive,args=(tcp_ip, alive_port))
        alive.start()
        while True:
            command = tcp.recv(1024)
            command = command.decode().strip()
            if command == "bye":
                tcp.close()
                break
            command = command.split()
            if command_list.get(command[0], 0) != 0:
                message = command_list[command[0]](command)
                send_message(message, tcp)
    except Exception as e:
        print("client disconnected.\n")
    try:
        tcp.close()
    except:
        pass
    try:
        tcp_keep_alive.close()
    except:
        pass
    tcp_keep_alive = 0
    tcp = 0

def keep_alive(tcp_ip, alive_port):
    time.sleep(1)
    global tcp, tcp_keep_alive
    tcp_keep_alive = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print((tcp_ip, alive_port))
    tcp_keep_alive.connect((tcp_ip, alive_port))
    try:
        while True:
            command = tcp_keep_alive.recv(1024)
            tcp_keep_alive.send(b"hello")
    except:
        pass
        
    try:
        tcp_keep_alive.close()
    except:
        pass
    try:
        tcp.close()
    except:
        pass
    tcp_keep_alive = 0
    tcp = 0
    

def send_message(string, client_socket):
    try:
        size = len(string)
        f = struct.pack("i", size)  # 打包fmt结构体
        client_socket.send(f)
        client_socket.sendall(string.encode('utf-8'))  # 编码
    except Exception as e:
        print(e)
    return


def receive_string(client_socket):
    data = ""
    try:
        d = client_socket.recv(struct.calcsize("i"))
        total_size = struct.unpack("i", d)
        num = total_size[0] // 1024
        for i in range(num):
            data += client_socket.recv(1024).decode('utf-8')
        data += client_socket.recv(total_size[0] % 1024).decode('utf-8')
    except Exception as e:
        print(e)
    return data

def start_listen(waiting_port, waiting_message):
    print("start client listen")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address = ("192.168.31.67", int(waiting_port))
    server_socket.bind(address)
    while True:
        receive_data, client = server_socket.recvfrom(1024)
        if receive_data.decode() == waiting_message.encode():
            break
    server_socket.close()
    print("client linking successfully, ip:{} port:{}".format(client[0],client[1]))
    return client[0]


if __name__ == "__main__":
    main()
