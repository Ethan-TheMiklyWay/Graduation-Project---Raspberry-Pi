import commons.mysql_connect as mysql_connect
from command.command_base.command_base import CommandBase


class GetCommand(CommandBase):
    def __init__(self):
        self.mysql_connector = mysql_connect.mysql_connector("sql_connect.txt")

    def execute(self, args):
        if len(args) == 1:
            if args[0] == "all":
                data = self.mysql_connector.select_all()
                return_data = []
                for row in data:
                    date = row[3]
                    info = [date.year, date.month, date.day, row[4], row[5], row[1], row[2]]
                    info = map(lambda x: str(x), info)
                    info = ",".join(info)
                    return_data.append(info)
                return ";".join(return_data)  # str(mysql_connector.select_all())
        else:
            return "parameter error"

