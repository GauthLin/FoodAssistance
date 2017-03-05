#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import pymysql.cursors
import sys

import param


class DBManager:
    def __init__(self):
        self.logger = logging.getLogger("food_assistance")

    def connect(self):
        try:
            connection = pymysql.connect(host='localhost',
                                         user=param.db['username'],
                                         password=param.db['password'],
                                         db='food_assistance',
                                         charset='utf8',
                                         cursorclass=pymysql.cursors.DictCursor)

            return connection
        except:
            self.logger.error("Unexpected error: %s", sys.exc_info()[1])
            return None

    def init(self):
        connection = self.connect()
        try:
            with connection.cursor() as cursor:
                sql = "CREATE DATABASE IF NOT EXISTS food_assistance"
                cursor.execute(sql)

            with connection.cursor() as cursor:
                sql = "CREATE TABLE IF NOT EXISTS food" \
                      "(id INT(11) PRIMARY KEY NOT NULL, name VARCHAR(20) NOT NULL, quantity DOUBLE DEFAULT '0', " \
                      "measuring_units VARCHAR(20))"
                cursor.execute(sql)

            with connection.cursor() as cursor:
                sql = "CREATE TABLE IF NOT EXISTS user(id INT(11) PRIMARY KEY NOT NULL,mail VARCHAR(255) NOT NULL)"
                cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()
        finally:
            connection.close()
