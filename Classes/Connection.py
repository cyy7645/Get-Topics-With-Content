#-*- coding:utf-8 -*-
# author:cyy7645
# datetime:2019-02-10 11:54
# software: PyCharm

import ssl
import urllib.request

# # create a fake agent
# class Connection:
#     def __init__(self):
#         ssl._create_default_https_context = ssl._create_unverified_context
#
#     def fakeAgent(self):
#         opener = urllib.request.build_opener()
#         opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#         return opener

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

    def get_data(self):
        self.cursor.execute("SELECT * FROM jobbole_article")
        rows = self.cursor.fetchall()
        for row in rows:
            fields = {}
            fields['title'] = row[0]
            fields['tags'] = row[8]
            fields['content'] = row[9]
            self.data[str(row[3])] = fields
        return self.data

    def insert_data(self, topics, url_object_id):
        insert_sql = """
                        UPDATE jobbole_article SET topics = %s 
                        WHERE url_object_id = %s
                    """
        params = (topics, url_object_id)
        self.cursor.execute(insert_sql, params)
        self.conn.commit()


if __name__ == '__main__':
    test = Connection()
    test.get_data()

