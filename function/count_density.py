# coding=utf-8
"""
人群密度计算模块
"""
import datetime

from sqlalchemy.sql import and_

from models import Station_passenger, Bus_passenger


def Count_station(timestamp_log, station_id_log):
    timestamp_log_f = datetime.datetime.strptime(timestamp_log, '%Y-%m-%d %H:%M:%S')  # 将字符串转换为datetime时间格式
    station_f = Station_passenger.query.filter(Station_passenger.timestamp == timestamp_log_f and
                                               Station_passenger.station_id == station_id_log).first()
    # station_f = Station_passenger.query.filter(and_(Station_passenger.timestamp == timestamp_log_f,
    #                                            Station_passenger.station_id == station_id_log)).first()

    # 若时间戳查询失败则时间往前一秒循环查询
    while station_f is None:
        timestamp_log_f = timestamp_log_f + datetime.timedelta(seconds=-1)  # 时间往前一秒
        # station_f = Station_passenger.query.filter(Station_passenger.timestamp == timestamp_log_f and
        #                                            Station_passenger.station_id == station_id_log).first()
        station_f = Station_passenger.query.filter(and_(Station_passenger.timestamp == timestamp_log_f,
                                                        Station_passenger.station_id == station_id_log)).first()

    timestamp_log_l = timestamp_log_f + datetime.timedelta(minutes=-5)  # 时间往前五分钟

    station_l = Station_passenger.query.filter(Station_passenger.timestamp == timestamp_log_l and
                                               Station_passenger.station_id == station_id_log).first()
    # station_l = Station_passenger.query.filter(and_(Station_passenger.timestamp == timestamp_log_l,
    #                                            Station_passenger.station_id == station_id_log)).first()

    # 若时间戳查询失败则时间往前一秒循环查询
    while station_l is None:
        timestamp_log_l = timestamp_log_l + datetime.timedelta(seconds=-1)
        # station_l = Station_passenger.query.filter(Station_passenger.timestamp == timestamp_log_l and
        #                                            Station_passenger.station_id == station_id_log).first()
        station_l = Station_passenger.query.filter(and_(Station_passenger.timestamp == timestamp_log_l,
                                                   Station_passenger.station_id == station_id_log)).first()

    count_station = int(station_f.station_passenger_id) - int(station_l.station_passenger_id) + 1
    return count_station


def Count_bus(timestamp_log, bus_id_log):
    timestamp_log_f = datetime.datetime.strptime(timestamp_log, '%Y-%m-%d %H:%M:%S')  # 将字符串转换为datetime时间格式
    bus_f = Bus_passenger.query.filter(Bus_passenger.timestamp == timestamp_log_f and
                                       Bus_passenger.bus_id == bus_id_log).first()
    # bus_f = Bus_passenger.query.filter(and_(Bus_passenger.timestamp == timestamp_log_f,
    #                                    Bus_passenger.bus_id == bus_id_log)).first()

    # 若时间戳查询失败则时间往前一秒循环查询
    while bus_f is None:
        timestamp_log_f = timestamp_log_f + datetime.timedelta(seconds=-1)  # 时间往前一秒
        bus_f = Bus_passenger.query.filter(Bus_passenger.timestamp == timestamp_log_f and
                                           Bus_passenger.bus_id == bus_id_log).first()
        # bus_f = Bus_passenger.query.filter(and_(Bus_passenger.timestamp == timestamp_log_f,
        #                                    Bus_passenger.bus_id == bus_id_log)).first()

    timestamp_log_l = timestamp_log_f + datetime.timedelta(minutes=-5)  # 时间往前五分钟

    bus_l = Bus_passenger.query.filter(Bus_passenger.timestamp == timestamp_log_l and
                                       Bus_passenger.bus_id == bus_id_log).first()
    # bus_l = Bus_passenger.query.filter(and_(Bus_passenger.timestamp == timestamp_log_l,
    #                                    Bus_passenger.bus_id == bus_id_log)).first()

    # 若时间戳查询失败则时间往前一秒循环查询
    while bus_l is None:
        timestamp_log_l = timestamp_log_l + datetime.timedelta(seconds=-1)
        bus_l = Bus_passenger.query.filter(Bus_passenger.timestamp == timestamp_log_l and
                                           Bus_passenger.bus_id == bus_id_log).first()
        # bus_l = Bus_passenger.query.filter(and_(Bus_passenger.timestamp == timestamp_log_l,
        #                                    Bus_passenger.bus_id == bus_id_log)).first()

    count_bus = int(bus_f.bus_passenger_id) - int(bus_l.bus_passenger_id) + 1
    return count_bus
