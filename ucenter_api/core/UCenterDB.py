#!/usr/bin/python
# _*_ coding:utf-8 _*_

import time
import pymysql
import yaml
from core.Logger import *

config_file = open('main_config/config.yml', 'r', encoding='utf-8')
config_variables = config_file.read()
conf = yaml.load(config_variables, Loader=yaml.FullLoader)

DB_HOST = conf.get('MYSQL_DB').get('DB_HOST')
DB_PORT = conf.get('MYSQL_DB').get('DB_PORT')
DB_USER = conf.get('MYSQL_DB').get('DB_USER')
DB_PASS = conf.get('MYSQL_DB').get('DB_PASS')
DATABASE = conf.get('MYSQL_DB').get('DATABASE')
DB_CONN_CHAR = conf.get('MYSQL_DB').get('DB_CONN_CHAR')

current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


class UCenterDB:
    @setup_log
    def __init__(self, host=DB_HOST,
                 port=DB_PORT,
                 user=DB_USER,
                 passwd=DB_PASS,
                 charset=DB_CONN_CHAR,
                 database=DATABASE):
        logging.info('u_center Database object Initialized.')
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.database = database
        self.charset = charset
        self.connect_database()
        logging.info('u_center Database Connected.')

    def connect_database(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    def clear_table(self, table):
        sql1 = "delete from %s" % table
        sql2 = "truncate table %s" % table
        cur = self.db.cursor()
        try:
            logging.info('Deleting data from table %s' % table)
            cur.execute(sql1)
        except Exception as e:
            logging.exception(e)
        try:
            logging.info('Truncating table %s' % table)
            cur.execute(sql2)
        except Exception as e:
            logging.exception(e)
        try:
            self.db.commit()
        except Exception as e:
            logging.error(e)
        cur.close()

    def insert_into_table(self, table, columns, rows=None):
        if rows is None:
            rows = []
        count = len(columns)
        s = "(%s"
        n = count - 1
        while n > 0:
            s = s + ",%s"
            n = n -1
        s = s+")"
        logging.info('Start inserting data to DB...')
        cur = self.db.cursor()
        for row in rows:
            sql = "insert into " + table + s % columns + " values" + s
            try:
                cur.execute(sql, row)
            except Exception as e:
                logging.exception(e)
        try:
            logging.info('Committing Data into Database...')
            self.db.commit()
            logging.info('Data committed. Data is stored in database: %s.%s' % (DATABASE, table))
        except Exception as e:
            logging.error('Inserting Data Error:', e)
            self.db.rollback()
        cur.close()
        self.close()
        return "Function insert_into_table END"

    def close(self):
        self.db.close()
