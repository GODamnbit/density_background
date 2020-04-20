# coding=utf-8
"""
公交信息发布模块：
1. 将人流信息的查询分为‘按公交ID查询’和‘按路线查询’，便于用户进行需求查询
    1）按公交ID查询：选择任意站点进行人流信息的查询
    2）按路线查询：选择任意路线同时可查看该路线各个站点的人流信息
2. 。。。
"""
import json
from flask import request, Blueprint, url_for, redirect
import op_db
from function.like import Add_like_bus
from models import Route, Bus
from flask_cors import *
from function.count_density import Count_bus

bus_server = Blueprint('bus_fabu', __name__)
CORS(bus_server, resources=r'/*')


@bus_server.route('/bus', methods=['GET', 'POST'])
def station_index():
    choose = request.values.get("query_way")
    if choose == '1':
        return redirect(url_for("bus_fabu.by_bus"))
    elif choose == '2':
        return redirect(url_for("bus_fabu.by_route_bus"))
    else:
        res = {
            'error_code': 200, 'msg': '这里是公交人群密度查询首页，请选择您的查询方式。'
        }
        return json.dumps(res, ensure_ascii=False)


@bus_server.route('/by_bus', methods=['GET', 'POST'])  # 按站点名查询
def by_bus_name():
    # now = datetime.now()
    bus_id_input = request.values.get('bus_id')
    color_input = request.values.get('color')
    if_like = request.values.get('if_like')  # 若收藏则为1
    if bus_id_input:
        bus = Bus.query.filter(Bus.bus_id == bus_id_input).first()

        if bus:
            # 当人群密度为Red时，人很多
            if color_input == "R":
                if if_like:
                    user_id_input = request.values.get('user_id')
                    timestamp = request.values.get('timestamp')
                    like = Add_like_bus(user_id_l=user_id_input, bus_id_l=bus_id_input, timestamp=timestamp)
                    context1 = {
                        'error_code': 201, 'msg': bus_id_input + '\n该公交人群密集！不建议乘坐这班公交！',
                        'if_like': like
                    }
                else:
                    context1 = {
                        'error_code': 201, 'msg': bus_id_input + '\n该公交人群密集！不建议乘坐这班公交！'
                    }
                return json.dumps(context1, ensure_ascii=False)

            # 当人群密度为Blue时，人较多
            elif color_input == "B":
                if if_like:
                    user_id_input = request.values.get('user_id')
                    timestamp = request.values.get('timestamp')
                    like = Add_like_bus(user_id_l=user_id_input, bus_id_l=bus_id_input, timestamp=timestamp)
                    context2 = {
                        'error_code': 202, 'msg': bus_id_input + '\n该公交人群不怎么多，可考虑乘坐这班公交。',
                        'if_like': like
                    }
                else:
                    context2 = {
                        'error_code': 202, 'msg': bus_id_input + '\n该公交人群不怎么多，可考虑乘坐这班公交。'
                    }
                return json.dumps(context2, ensure_ascii=False)

            # 当人群密度为Green时，人少
            elif color_input == "G":
                if if_like:
                    user_id_input = request.values.get('user_id')
                    timestamp = request.values.get('timestamp')
                    like = Add_like_bus(user_id_l=user_id_input, bus_id_l=bus_id_input, timestamp=timestamp)
                    context3 = {
                        'error_code': 203, 'msg': bus_id_input + '\n该公交人很少，很建议乘坐这班公交哦~',
                        'if_like': like
                    }
                else:
                    context3 = {
                        'error_code': 203, 'msg': bus_id_input + '\n该公交人很少，很建议乘坐这班公交哦~'
                    }
                return json.dumps(context3, ensure_ascii=False)
        else:
            res = {
                'error_code': 204, 'msg': '抱歉，暂时还没有该公交信息，我们会及时补充~'
            }
            return json.dumps(res, ensure_ascii=False)
    else:
        res = {
            'error_code': 205, 'msg': '欢迎来到公交查询！请输入要查询的公交ID！'
        }
        return json.dumps(res, ensure_ascii=False)


@bus_server.route('/by_route_bus', methods=['GET', 'POST'])  # 按路线查询
def by_route_bus():
    route_name_input = request.values.get('route_name')
    timestamp_input = request.values.get('timestamp')
    if route_name_input and timestamp_input:
        # 获取指定路线信息
        route = Route.query.filter(Route.route_name == route_name_input).first()
        if route:  # 若该路线存在
            route_id_need = route.route_id
            # print(route_id_need)
            sql = "SELECT COUNT((bus_id)) FROM bus WHERE route_id='%s';" % route_id_need
            result = op_db.login_add(sql)  # 执行sql
            # 获取路线所包含的站点数
            length = result[0].get('COUNT((bus_id))')
            bus_need = Bus.query.filter(Bus.route_id == route_id_need).first()
            begin_id = bus_need.bus_id
            # 以列表形式向前端输出该路线各个公交的人群密度信息
            res_list = []
            i = 1
            while i <= length:
                bus = Bus.query.filter(Bus.bus_id == begin_id).first()
                if bus:
                    # bus_then = Station.query.filter(Station.station_id == i).first()
                    # station_name = station_then.station_name
                    density = Count_bus(timestamp_log=timestamp_input, bus_id_log=begin_id)
                    res_dic = {
                        'bus_id': begin_id, 'density': density
                    }
                    res_list.append(res_dic)
                begin_id += 1
                i += 1
            return json.dumps(res_list, ensure_ascii=False)
        else:
            res = {
                'error_code': 405, 'msg': '抱歉暂无该路线信息！'
            }
            return json.dumps(res, ensure_ascii=False)
    else:
        res = {
            'error_code': 404, 'msg': '关键参数未填！'
        }
        return json.dumps(res, ensure_ascii=False)
