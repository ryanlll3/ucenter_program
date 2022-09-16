#!/usr/bin/python
# _*_ coding:utf-8 _*_

import logging
from logging.handlers import RotatingFileHandler


def setup_log(func):
    """配置日志"""
    # 设置日志的记录等级(# FATAL/CRITICAL = 重大的，危险的(50)
    # WARNING = 警告(40)
    # ERROR = 错误(30)
    # INFO = 信息(20)
    # DEBUG = 调试(10)
    logging.basicConfig(level=20)
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限

    file_log_handler = RotatingFileHandler("logs/ucenter.log",
                                           maxBytes=1024 * 1024 * 100, backupCount=10)
    #1 KB = 1024 bytes
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(asctime)s %(levelname)s File:%(module)s Line:%(lineno)d Message:%(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象,添加日志记录器
    logging.getLogger().addHandler(file_log_handler)

    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper

