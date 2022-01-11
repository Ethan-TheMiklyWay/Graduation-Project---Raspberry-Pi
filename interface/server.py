# encoding=UTF-8

import socket
from keep_alive import start_finding


def main():
    init_command()
    start_finding(interview=1, port=8000)
    start_listen("0.0.0.0", 8080)


def init_command():
    from command.get import GetCommand
    from command.node import NodeCommand

    global command_list
    command_list = dict()
    command_list["get"] = GetCommand()
    command_list["node"] = NodeCommand()


def start_listen(ip, port):
    print("start client listen")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(10)
    while True:
        client_socket, clientAddr = server_socket.accept()
        recv_data = client_socket.recv(1024).decode('gbk')
        print("client address: {}, question string: {}".format(str(clientAddr), recv_data))

        command = recv_data.split()
        if command_list.get(command[0]):
            try:
                return_msg = command_list[command[0]].execute(command[1:])
            except Exception as e:
                return_msg = "error:" + str(e)
        else:
            return_msg = "error: command is not valid"
        client_socket.send(return_msg.encode())


if __name__ == "__main__":
    main()
