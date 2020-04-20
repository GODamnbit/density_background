import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from vision.choose_data import sql_connect_station_passenger
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import time
import datetime



def get_data_frame(data_list):
    # 将从数据库获取的数据转化成二维数组DataFrame()
    temp_df = pd.DataFrame(data_list)
    # 把timestamp变成时间格式
    temp_df["timestamp"] = pd.to_datetime(temp_df["timestamp"])
    # 删除重复数据
    temp_df = temp_df.drop_duplicates(keep='last')
    return temp_df

def str_datetime_frame(a):
    # 将请求的时间字符串转换为datetime类型
    # 将其转换为时间数组
    timeArray = time.strptime(a,"%Y-%m-%d %H:%M:%S")
    # 再将时间数组转换为时间戳
    timeStamp = time.mktime(timeArray)
    # 将时间戳转化为datetime类型
    date = datetime.datetime.fromtimestamp(timeStamp)
    return date

def normaltime(datetime1):
    # 将时间字符串转化为datetime类型
    normaltime = datetime.datetime.strptime(datetime1,'%Y-%m-%d %H:%M:%S')
    return normaltime


if __name__ == '__main__':
    # SQL = "SELECT * FROM bus_passenger;"
    # data_list = choose_data(SQL)
    # for i in data_list:
    #     print(i["bus_id"],"***",i["timestamp"])
    # print(data_list)
    data1 = get_data_frame(sql_connect_station_passenger())
    print(data1)
    a = "2020-04-06 16:30:00"
    time = str_datetime_frame(a)
    print(time)
    time2 = normaltime(a)
    print(time2)
    print(type(time2))
