#!/usr/bin/python3
import pymysql
import warnings
import settings
class Database:

    def __init__(self):
        self.db = pymysql.connect("localhost","python", "CuloMadonna19@__", "telegram_message_IDs" )
        cursor = self.db.cursor()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sql = """CREATE TABLE IF NOT EXISTS telegram_message_IDs (
                        id INT AUTO_INCREMENT NOT NULL,
                        message_id VARCHAR(64) NOT NULL,
                        full_name VARCHAR(64) NOT NULL,
                        name VARCHAR(64) NOT NULL,
                        PRIMARY KEY(id)
                    )"""

            try:
                cursor.execute(sql)
                self.db.commit()
            except:
                self.db.rollback()
                print("Couldn't create table:")

    def detect_empty_table(self):
        sql = """ SELECT id FROM telegram_message_IDs """
        cursor = self.db.cursor()
        cursor.execute(sql)
        return True if cursor.fetchone() == None else 0

    def insert(self, message_id, full_name="", name=""):
        """ Insert a new entry into the table """
        # we create a string from which we will generate a hash to uniquely
        # identify a table row
        sql = """ INSERT INTO telegram_message_IDs (message_id, full_name, name)
                VALUES ("{}", "{}", "{}")
                """.format(message_id, full_name, name)
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
            ret = 0
        except:
            self.db.rollback()
            ret = 1
        return ret

    def load_entries(self):
        """ Retrieves the whole telegram_message_IDs table as a list. Such list is the one
            returned by cursor.fetchall()
        """
        sql = """SELECT message_id, full_name, name FROM telegram_message_IDs"""
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def update(self, message_id, name):
        retval = False
        sql = f""" SELECT name FROM telegram_message_IDs WHERE name='{name}'; """
        cursor = self.db.cursor()
        cursor.execute(sql)
        if(cursor.fetchone() == None):
            sql = f""" INSERT INTO telegram_message_IDs (message_id, full_name, name) VALUES
                    ('{message_id}', '{settings.NAMES[name]}', '{name}') """
            try:
                cursor.execute(sql)
                self.db.commit()
                retval = True
            except:
                self.db.rollback()
        else:
            sql = f""" UPDATE telegram_message_IDs SET message_id='{message_id}', name='{name}', full_name='{settings.NAMES[name]}'
                WHERE name='{name}'; """
            try:
                cursor.execute(sql)
                self.db.commit()
                retval = True
            except:
                self.db.rollback()
        return retval

    def quit(self):
        """ Close the connetion to the mysql database """
        self.db.close()
