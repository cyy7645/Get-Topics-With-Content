# import re
# f = open("/Users/cyy7645/Desktop/test.html", "r")
# text = f.read()
#
# regex_str = "<[^>]+>|&.{1,10};"
# matchObj = re.sub(regex_str, '', text)
# # for String in matchObj:
# #     if String.startswith('<'):
# #         matchObj.remove(String)
# print(type(matchObj))


import pymysql
from Classes.Constants import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWORD, PORT

# connect to MySQL
class Connection:
    def __init__(self):
        # setting for mysql
        self.conn = pymysql.connect(host=MYSQL_HOST, port=PORT,
                                    user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                    db=MYSQL_DBNAME, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        # key: url_object_id  value: dict (contains title, tags, content)
        self.data = {}

    def insert_data(self):
        self.cursor.execute('UPDATE jobbole_article SET keywords = "hahah" WHERE url_object_id = "00300456460ea6d4134a02e6861bd127"')

if __name__ == "__main__":
    test = Connection()
    test.insert_data()
