# encoding=UTF-8
"""
tools used for read and write configuration file
"""
import os
import io


def get_server_ini(path):
    """
    :param path: the ini file path.
    :return: a dict structure
        eg: {"pi_id": 1, "db_connect_file": "sql_connect.txt"}
    """
    path = str(path)
    assert type(path) is str
    if not os.path.exists(path):
        raise Exception("init file is not exist")

    info = {}
    error_in_file = 0
    with io.open(path, encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip() == "" or line.strip()[0] == "#":
                continue
            try:
                text = line.split("=", 1)
                item = text[0].strip()
                cont = text[1].strip()
                info[item] = cont
            except:
                error_in_file = 1
    if error_in_file:
        raise Exception("init file format error")

    return info


def save_server_int(path, content):
    """
    used to save configuration
    :param path: configuration path
    :param content: a dict structure
        eg: {"pi_id": 1, "db_connect_file": "sql_connect.txt"}
    :return: None
    """
    assert type(content) is dict
    content = dict(content)
    with io.open(path, "w") as file:
        for item in content.keys():
            file.write((item + "=" + str(content[item]) + "\n").decode())


def find_lan_ip_address():
    """
    used to find local area net ip. only in linux system
    :return: LAN ip address
    """
    for line in os.popen('/sbin/route').readlines():
        
        if "192.168" in line:
            net = line.split()[0]
            if len(net.split(".")) == 4:
                return net
    return 0

if __name__=="__main__":
    print(find_lan_ip_address())
