# encoding=UTF-8
"""
mysql_connector used to connect mysql
"""

import pymysql.cursors
import os
import time


class mysql_connector:
    def __init__(self, connect_file):
        """
        this class used to connect mysql
        :param connect_file: configuration file path for connect mysql
        """
        self.__connect_file = connect_file
        self.__info = self.__get_connect_info(connect_file)
        db_delete = "DELETE FROM iot_info WHERE {} = {}"

        db_update = "UPDATE iot_info SET {} = {} WHERE {} = {}"
        self.__update_syntax = db_update
        self.__delete_syntax = db_delete

    def select_all(self):
        sql = "SELECT * FROM iot_info;"
        return self.__select_with_sql(sql)

    def select_primary_key(self):
        sql = "SELECT id FROM iot_info;"
        prim_key = self.__select_with_sql(sql)
        prim_set = set()
        for row in prim_key:
            prim_set.add(row[0])
        return prim_set

    def insert_localhost_with_check(self, data):
        primarykey = self.select_primary_key()
        insert_data_set = []
        for row in data:
            if row[0] not in primarykey:
                insert_data_set.append(row)

        db_insert = "INSERT INTO iot_info " \
                    "(id, pi_id, nodemcu_id, time, temperature, moisture, retrieve, other) " \
                    "VALUES ( '{}', '{}', '{}', '{}', {}, {}, {}, '{}' )"
        connect = self.__get_connect()
        cursor = connect.cursor()
        for data in insert_data_set:
            self.insert_localhost(data, cursor)
        connect.commit()
        cursor.close()
        connect.close()

    def __get_connect(self):
        connect = pymysql.Connect(
            host=self.__info["host"],
            port=int(self.__info["port"]),
            user=self.__info["user"],
            passwd=self.__info["passwd"],
            db=self.__info["db"],
            charset=self.__info["charset"]
        )
        return connect

    def insert_localhost(self, content, sql_cursor):
        db_insert = "INSERT INTO iot_info " \
                    "(id, pi_id, nodemcu_id, time, temperature, moisture, retrieve, other) " \
                    "VALUES ( '{}', '{}', '{}', '{}', {}, {}, {}, '{}' )"
        insert_data = list()
        insert_data.append(content[0])
        insert_data.append(content[1])
        insert_data.append(content[2])
        insert_data.append(content[3])
        insert_data.append(content[4])
        insert_data.append(content[5])
        insert_data.append(0)
        insert_data.append(content[7])
        sql = db_insert.format(*insert_data)
        sql_cursor.execute(sql)
        pass

    def insert(self, content):
        db_insert = "INSERT INTO iot_info " \
                    "(id, pi_id, nodemcu_id, time, temperature, moisture, retrieve, other) " \
                    "VALUES ( '{}', '{}', '{}', '{}', {}, {}, {}, '{}' )"
        insert_data = []
        time_now = time.localtime()
        time_id = time.strftime("%Y%m%d%H%M%S", time_now)
        insert_id = content["pi_id"] + content["nodemcu_id"] + time_id
        insert_data.append(insert_id)
        insert_data.append(content["pi_id"])
        insert_data.append(content["nodemcu_id"])
        time_date = time.strftime("%Y-%m-%d %H:%M:%S", time_now)
        insert_data.append(time_date)
        insert_data.append(content["temperature"])
        insert_data.append(content["moisture"])
        insert_data.append(0)
        insert_data.append(0)
        sql = db_insert.format(*insert_data)
        connect = pymysql.Connect(
            host=self.__info["host"],
            port=int(self.__info["port"]),
            user=self.__info["user"],
            passwd=self.__info["passwd"],
            db=self.__info["db"],
            charset=self.__info["charset"]
        )
        cursor = connect.cursor()
        cursor.execute(sql)
        connect.commit()
        cursor.close()
        connect.close()

    def __select_with_sql(self, sql):
        result = 0
        try:
            connect = pymysql.Connect(
                host=self.__info["host"],
                port=int(self.__info["port"]),
                user=self.__info["user"],
                passwd=self.__info["passwd"],
                db=self.__info["db"],
                charset=self.__info["charset"]
            )
            cursor = connect.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            connect.commit()
            cursor.close()
            connect.close()
        except Exception as e:
            print(e)
        try:
            connect.close()
        except:
            pass
        return result

    def test_link(self):
        """
        test for mysql link
        :return: None
        """
        connect = pymysql.Connect(
            host=self.__info["host"],
            port=int(self.__info["port"]),
            user=self.__info["user"],
            passwd=self.__info["passwd"],
            db=self.__info["db"],
            charset=self.__info["charset"]
        )
        connect.close()

    def __get_connect_info(self, path):
        if not os.path.exists(path):
            raise Exception("database link file did not exist")

        info = {"host": 0, "port": 0, "user": 0, "passwd": 0, "db": 0, "charset": 0}
        error_in_file = 0
        with open(path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == "":
                    continue
                try:
                    text = line.split(":", 1)
                    item = text[0].strip()
                    cont = text[1].strip()
                    info[item] = cont
                except:
                    error_in_file = 1
        if error_in_file:
            raise Exception("the format in the database link file is not correct")

        error_in_key = 0
        for content in info.keys():
            if info[content] == 0:
                error_in_key = 1
                break
        if error_in_key:
            raise Exception("incomplete in database link file")
        return info
