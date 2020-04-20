# coding=utf-8
"""
数据可视化模块接口：
1. 将station_id，start_time，end_time传输给可视化模块
2. 将HTML图表返回给前端
"""
import json
from flask import Blueprint, request
from flask_cors import CORS
from vision.bus_data_overview import show_bus_date_overview_mpl, show_bus_date_overview_ply
from vision.bus_passengers_count import bus_passengers_count_, show_bus_passengers_count_mpl, \
    show_bus_passengers_count_ply
from vision.different_station_count import different_station_count_, show_different_station_count_mpl, \
    show_different_station_count_ply
from vision.station_data_overview import show_station_date_overview_mpl, show_station_date_overview_ply
from vision.station_passengers_count import station_passengers_count_, show_station_passengers_count_mpl, \
    show_station_passengers_count_ply

vision_server = Blueprint('station_vision', __name__)
CORS(vision_server, resources=r'/*')


@vision_server.route('/vision', methods=['GET', 'POST'])
def vision():
    request_way = request.values.get("request_way")
    start_time = request.values.get("start_time")
    end_time = request.values.get("end_time")
    bus_id = request.values.get("bus_id")
    station_id = request.values.get("station_id")
    if request_way == '1':
        """不同公交路线的人群数量随时间的变化情况折线图"""
        # show_bus_date_overview_mpl(start_date=str(start_time), end_date=str(end_time))
        res = {"status": 200, "html": show_bus_date_overview_ply(start_date=str(start_time), end_date=str(end_time))}
        return json.dumps(res, ensure_ascii=False)

    if request_way == '2':
        """某路公交车上人群数量随时间的变化情况折线图"""
        # bus_passengers_count_(bus_id=int(bus_id), start_date=str(start_time), end_date=str(end_time))
        # show_bus_passengers_count_mpl(bus_id=int(bus_id), start_date=str(start_time), end_date=str(end_time))
        res = {"status": 200, "html": show_bus_passengers_count_ply(bus_id=int(bus_id), start_date=str(start_time),
                                                                    end_date=str(end_time))}
        return json.dumps(res, ensure_ascii=False)

    if request_way == '3':
        """某段时间内不同站台的人群数量统计直方图"""
        # different_station_count_(start_date=str(start_time), end_date=str(end_time))
        # show_different_station_count_mpl(start_date=str(start_time), end_date=str(end_time))
        res = {"status": 200, "html": show_different_station_count_ply(start_date=str(start_time), end_date=str(end_time))}
        return json.dumps(res, ensure_ascii=False)

    if request_way == '4':
        """不同站台的人群数量随时间的变化情况折线图"""
        # show_station_date_overview_mpl(start_date=str(start_time), end_date=str(end_time))
        res = {"status": 200, "html": show_station_date_overview_ply(start_date=str(start_time), end_date=str(end_time))}
        return json.dumps(res, ensure_ascii=False)

    if request_way == '5':
        """某号站台的人群数量随时间的变化情况折线图"""
        # station_passengers_count_(station_id=int(station_id), start_date=str(start_time), end_date=str(end_time))
        # show_station_passengers_count_mpl(station_id=int(station_id), start_date=str(start_time),\
        # end_date=str(end_time))
        res = {"status": 200, "html": show_station_passengers_count_ply
        (station_id=int(station_id), start_date=str(start_time), end_date=str(end_time))}
        return json.dumps(res, ensure_ascii=False)
