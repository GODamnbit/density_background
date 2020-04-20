# coding=utf-8
"""
站点信息发布模块：
1. 将人流信息的查询分为‘按站点查询’和‘按路线查询’，便于用户进行需求查询
    1）按站点查询：选择任意站点进行人流信息的查询
    2）按路线查询：选择任意路线同时可查看该路线各个站点的人流信息
2. 。。。
"""
import json
from flask import request, Blueprint, url_for, redirect
from datetime import datetime
import op_db
from function.like import Add_like_station
from models import Station, Route, Route_station
from flask_cors import *
from function.count_density import Count_station

station_server = Blueprint('station_fabu', __name__)
CORS(station_server, resources=r'/*')


@station_server.route('/station', methods=['GET', 'POST'])
def station_index():
    choose = request.values.get("query_way")
    if choose == '1':
        return redirect(url_for("station_fabu.by_station_name"))
    elif choose == '2':
        return redirect(url_for("station_fabu.by_route_station"))
    else:
        res = {
            'error_code': 200, 'msg': '这里是地铁站台人群密度查询首页，请选择您的查询方式。'
        }
        return json.dumps(res, ensure_ascii=False)


@station_server.route('/by_station_name', methods=['GET', 'POST'])  # 按站点名查询
def by_station_name():
    now = datetime.now()
    station_name_input = request.values.get('station_name')
    color_input = request.values.get('color')
    if_like = request.values.get('if_like')
    if station_name_input:
        station_name = Station.query.filter(Station.station_name == station_name_input).first()
        s_id = station_name.station_id
        print(s_id)

        if station_name:
            # 当人群密度为Red时，人很多
            if color_input == "R":
                if if_like:
                    user_id_input = request.values.get('user_id')
                    timestamp = request.values.get('timestamp')
                    like = Add_like_station(user_id_l=user_id_input, station_id_l=s_id, timestamp=timestamp)
                    context1 = {
                        'error_code': 201, 'msg': station_name_input + '\n' + str(now)
                        + '\n该站点人群密集！不建议由此站点出行！', 'imageUrl': './static/images/R.jpg',
                        'if_like': like
                    }
                else:
                    context1 = {
                        'error_code': 201, 'msg': station_name_input + '\n' + str(now)
                        + '\n该站点人群密集！不建议由此站点出行！', 'imageUrl': './static/images/R.jpg'
                    }
                return json.dumps(context1, ensure_ascii=False)

            # 当人群密度为Blue时，人较多
            elif color_input == "B":
                if if_like:
                    user_id_input = request.values.get('user_id')
                    timestamp = request.values.get('timestamp')
                    like = Add_like_station(user_id_l=user_id_input, station_id_l=s_id, timestamp=timestamp)
                    context2 = {
                        'error_code': 202, 'msg': station_name_input + '\n' + str(now)
                        + '\n该站点人群不怎么多，可考虑由此站点出行。', 'imageUrl': './static/images/B.jpg',
                        'if_like': like
                    }
                else:
                    context2 = {
                        'error_code': 202, 'msg': station_name_input + '\n' + str(now)
                        + '\n该站点人群不怎么多，可考虑由此站点出行。', 'imageUrl': './static/images/B.jpg'
                    }
                return json.dumps(context2, ensure_ascii=False)

            # 当人群密度为Green时，人少
            elif color_input == "G":
                if if_like:
                    user_id_input = request.values.get('user_id')
                    timestamp = request.values.get('timestamp')
                    like = Add_like_station(user_id_l=user_id_input, station_id_l=s_id, timestamp=timestamp)
                    context3 = {
                        'error_code': 203, 'msg': station_name_input + '\n' + str(now)
                        + '\n该站点人很少，很建议由此站点出行哦~', 'imageUrl': './static/images/G.jpg',
                        'if_like': like
                    }
                else:
                    context3 = {
                        'error_code': 203, 'msg': station_name_input + '\n' + str(now)
                        + '\n该站点人很少，很建议由此站点出行哦~', 'imageUrl': './static/images/G.jpg'
                    }
                return json.dumps(context3, ensure_ascii=False)
        else:
            res = {
                'error_code': 204, 'msg': '抱歉，暂时还没有该站点信息，我们会及时补充~'
            }
            return json.dumps(res, ensure_ascii=False)
    else:
        res = {
            'error_code': 205, 'msg': '欢迎来到站点查询！请输入要查询的站点名！'
        }
        return json.dumps(res, ensure_ascii=False)


@station_server.route('/by_route_station', methods=['GET', 'POST'])  # 按路线查询
def by_route_station():
    route_name_input = request.values.get('route_name')
    timestamp_input = request.values.get('timestamp')
    if route_name_input and timestamp_input:
        route = Route.query.filter(Route.route_name == route_name_input).first()
        if route:
            sql = "SELECT COUNT((station_id)) FROM route_station;"
            result = op_db.login_add(sql)  # 执行sql
            length = result[0].get('COUNT((station_id))')
            i = 1
            # 循环查询该路线所有站点的人群密度信息
            res_list = []
            while i <= length:
                # 首先查询路线站点列表是否有该站点的存在
                station = Route_station.query.filter(Route_station.station_id == i).first()
                if station:  # 若存在，则返回密度信息
                    station_then = Station.query.filter(Station.station_id == i).first()
                    station_name = station_then.station_name
                    density = Count_station(timestamp_log=timestamp_input, station_id_log=i)
                    res_dic = {
                        'station_name': station_name, 'density': density
                    }
                    res_list.append(res_dic)
                i += 1
            return json.dumps(res_list, ensure_ascii=False)
        else:
            res = {
                'error_code': 404, 'msg': '抱歉暂无该路线信息！'
            }
            return json.dumps(res, ensure_ascii=False)
