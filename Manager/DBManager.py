import pymysql.cursors


class DBManager:
    def connect(self):
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     db='food_assistance',
                                     charset='utf8',
                                     cursorclass=pymysql.cursors.DictCursor)

        return connection

