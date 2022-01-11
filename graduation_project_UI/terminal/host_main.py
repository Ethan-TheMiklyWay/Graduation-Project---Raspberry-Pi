# encoding=UTF-8
""""
python 3.7
main function in windows host
essential libraries for this program are listed as follow:
    pymysql: connect to mysql
"""
from terminal.command_translate import Execute
import sys

host_ini = "host.ini"


def main():
    try:
        exe = Execute(host_ini)
    except Exception as e:
        print("fatal error happen :", str(e))
        sys.exit(1)

    print("type help to get more information\n")
    while True:
        try:
            if not exe.execute(input(">>")):
                break
        except Exception as e:
            print(str(e))
    exe.terminate()


if __name__ == "__main__":
    main()
