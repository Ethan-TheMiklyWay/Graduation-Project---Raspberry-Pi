# encoding=UTF-8
import os
import subprocess
import tools

server_ini_path = "server.ini"


def main():
    close_mosquitto()
    close_pyprogress()


def close_pyprogress():
    child = subprocess.Popen(["pgrep", "-f", "python"], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0].split()
    for each in response:
        os.system("kill -KILL " + str(each))

    child = subprocess.Popen(["pgrep", "-f", "sh"], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0].split()
    for each in response:
        os.system("kill -KILL " + str(each))


def close_mosquitto():
    child = subprocess.Popen(["pgrep", "-f", "mosquitto"], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0].split()
    for each in response:
        os.system("kill -KILL " + str(each))


if __name__ == "__main__":
    main()
