# encoding=UTF-8

"""
used to link raspberry pi
"""

import os
import threading
import time
import socket
import datetime
import struct


class Link:
    def __init__(self, searchtime, mqtt_port, tcp_port, mqtt_content, tcp_timeout, tcp_keep_port):
        """
        init raspberry pi link
        :param searchtime: search interview for mqtt service
        :param mqtt_port: search mqtt port
        :param tcp_port: open tcp service port
        """
        self.__search_time = searchtime
        self.__mqtt_port = mqtt_port
        self.__tcp_port = tcp_port
        self.__mqtt_content = mqtt_content

        self.__link_state = 0  # tcp连接是否成功
        self.__search_state = 0  # 是否开启mqtt寻找
        self.__listen_tcp = 0  # tcp端口是否绑定
        self.__mqtt_ip = 0  # 获取的mqtt服务器地址
        self.__tcp = 0  # tcp的socket对象
        self.__connect = 0  # 当前tcp连接对象
        self.__tcp_timeout = tcp_timeout
        self.__timeout_stamp = dict()
        self.__tcp_keep_port = tcp_keep_port

    def get_windows_ip(self):
        ip = 0
        for line in os.popen('route print').readlines():
            if "0.0.0.0" in line and len(line.split()[-3].split(".")) == 4:
                ip = line.split()[-2]
        return ip

    def get_link_state(self):
        return self.__link_state

    def get_mqtt_ip(self):
        return self.__mqtt_ip

    def get_searching_state(self):
        return self.__search_state

    def open_listen(self, ip):
        if self.__listen_tcp != 0:
            return
        listen = threading.Thread(target=self.__tcp_open, args=(ip,))
        listen.start()

    def close_tcp(self):
        if self.__tcp == 0:
            return
        try:
            self.__connect.send(b"bye")
            self.__connect.close()
        except:
            pass
        try:
            self.__tcp.close()
        except:
            pass

        try:
            self.__keep_alive_connect.close()
        except:
            pass
        try:
            self.__keep_alive_tcp.close()
        except:
            pass
        self.__tcp = 0
        self.__link_state = 0
        self.__connect = 0
        self.__search_state = 0
        self.__listen_tcp = 0
        self.terminate_searching()


    def __receive_string(self, client_socket):
        data = ""
        try:
            d = client_socket.recv(struct.calcsize("i"))
            total_size = struct.unpack("i", d)
            num = total_size[0] // 1024
            for i in range(num):
                temp_data = client_socket.recv(1024).decode('utf-8')
                data += temp_data
            temp_data = client_socket.recv(1024).decode('utf-8')
            data += temp_data
        except Exception as e:
            pass
        return data

    def __tcp_open(self, ip):
        self.__listen_tcp = 1
        self.__tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__tcp.bind((ip, self.__tcp_port))
        self.__tcp.listen(1)
        try:
            self.__connect, self.__mqtt_ip = self.__tcp.accept()
        except:
            pass
        print('\b\b\b\b\nmqtt server {} connected\n>>'.format(str(self.__mqtt_ip)), end="")
        self.__link_state = 1
        listen = threading.Thread(target=self.__tcp_keep_alive)
        listen.start()

    def __tcp_keep_alive(self):
        ip = self.get_windows_ip()
        address = (ip, self.__tcp_keep_port)
        self.__keep_alive_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__keep_alive_tcp.bind(address)
        self.__keep_alive_tcp.listen(5)
        self.__keep_alive_connect, keep_alive_addr = self.__keep_alive_tcp.accept()
        self.__keep_alive_connect.settimeout(2)
        try:
            while True:
                time.sleep(2)
                self.__keep_alive_connect.send(b"hello")
                if not self.__keep_alive_connect.recv(1024):
                    print("raspberry disconnected")
                    break
        except Exception as e:
            pass
        try:
            self.__keep_alive_connect.close()
        except:
            pass
        try:
            self.__keep_alive_tcp.close()
        except:
            pass
        self.close_tcp()

    def tcp_communication(self, command, set_time_out=False):
        if self.__tcp == 0:
            raise Exception("tcp is not established")
        if self.__connect == 0:
            raise Exception("mqtt connect is not established")
        self.__send_message(str(command), self.__connect)

        timestamp = time.time()
        self.__timeout_stamp[timestamp] = 1
        if set_time_out:
            listen = threading.Thread(target=self.__set_tcp_time_out, args=(timestamp,))
            listen.start()
        receive = self.__receive_string(self.__connect)
        try:
            del self.__timeout_stamp[timestamp]
        except:
            pass
        return receive

    def __set_tcp_time_out(self, timestamp):
        time.sleep(self.__tcp_timeout)
        if self.__timeout_stamp.get(timestamp, 0) == 1:
            try:
                self.close_tcp()
            except:
                pass
            try:
                del self.__timeout_stamp[timestamp]
            except:
                pass
            print("time out, trying to reconnect, tcp link close")

    def __send_message(self, string, client_socket):
        try:
            size = len(string)
            f = struct.pack("i", size)  # 打包fmt结构体
            client_socket.send(f)
            client_socket.sendall(string.encode('utf-8'))  # 编码
        except Exception as e:
            pass
            # (e)
        return

    def start_searching(self, ip):
        if self.__search_state == 1:
            return
        if self.__link_state == 1:
            return
        self.__search_state = 1
        searching = threading.Thread(target=self.__searching, args=(ip,))
        searching.start()

    def terminate_searching(self):
        self.__search_state = 0

    def __searching(self, ip):
        self.__single_search(ip)
        last_time = time.time()
        while True:
            if self.__search_state == 0:
                break
            if self.__link_state == 1:
                break
            if time.time() - last_time > self.__search_time:
                self.__single_search(ip)
                last_time = time.time()
            time.sleep(1)
        pass

    def __single_search(self, ip):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        search_base = ip.rsplit(".", 1)[0] + "."
        for i in range(1, 254):
            search_ip = search_base + str(i)
            msg = self.__mqtt_content.encode()
            server_address = (search_ip, int(self.__mqtt_port))
            client_socket.sendto(msg, server_address)  # 将msg内容发送给指定接收方
        client_socket.close()
