import os
"""数据库配置信息"""
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'Hello@world'
HOST = '123.57.55.107'
PORT = '3306'
DATABASE = 'PopulationDensity'
DEBUG = True
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD,
                                                                       HOST, PORT, DATABASE)
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 动态追踪修改设置，如未设置只会提示警告
BASE_PATH = os.getcwd().replace('//', r'//')
