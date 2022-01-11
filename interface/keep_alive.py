import socket
import threading
import time


def start_finding(interview, port=8000):
    threading.Thread(target=send_hello, args=(interview, port)).start()


def send_hello(interview, PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    msg = b"hello"
    server_address = ("255.255.255.255", PORT)
    while True:
        try:
            client_socket.sendto(msg, server_address)
        except Exception as e:
            print("error happened: {}".format(str(e)))
        time.sleep(interview)
