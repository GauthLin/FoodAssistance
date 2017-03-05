#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import sys

from Manager.DBManager import DBManager


class UserRepository:
    def __init__(self):
        self.db_manager = DBManager()
        self.logger = logging.getLogger('food_assistance')

    def get_users_mails(self):
        connection = self.db_manager.connect()
        try:
            with connection.cursor() as cursor:
                sql = 'SELECT mail FROM user'
                cursor.execute(sql)
                mails = []
                for row in cursor.fetchall():
                    mails.append(row['mail'])
        except:
            self.logger.error("Unexpected error: %s", sys.exc_info()[1])
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

            self.logger.info("L'adresse mail `%s` a bien été ajouté à la liste des utilisateurs.", mail)
        except:
            self.logger.error("Unexpected error: %s", sys.exc_info()[1])
        finally:
            connection.close()

    def del_mail(self, mail):
        connection = self.db_manager.connect()
        try:
            with connection.cursor() as cursor:
                sql = 'DELETE FROM user WHERE mail=%s'
                cursor.execute(sql, mail)

            connection.commit()

            self.logger.info("L'adresse mail `%s` a bien été supprimé de la liste des utilisateurs.", mail)
        except:
            self.logger.error("Unexpected error: %s", sys.exc_info()[1])
        finally:
            connection.close()
