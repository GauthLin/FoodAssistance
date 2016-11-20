from Manager.DBManager import DBManager


class UserRepository:
    def __init__(self):
        self.db_manager = DBManager()

    def get_users_mails(self):
        connection = self.db_manager.connect()
        try:
            with connection.cursor() as cursor:
                sql = 'SELECT mail FROM user'
                cursor.execute(sql)
                mails = []
                for row in cursor.fetchall():
                    mails.append(row['mail'])
        finally:
            connection.close()

        return mails

    def add_mail(self, mail):
        connection = self.db_manager.connect()
        try:
            with connection.cursor() as cursor:
                sql = 'INSERT INTO user (mail) VALUES (%s)'
                cursor.execute(sql, mail)

            connection.commit()
        finally:
            connection.close()

    def del_mail(self, mail):
        connection = self.db_manager.connect()
        try:
            with connection.cursor() as cursor:
                sql = 'DELETE FROM user WHERE mail=%s'
                cursor.execute(sql, mail)

            connection.commit()
        finally:
            connection.close()
