# coding=utf-8
"""
管理员模块
1. 对用户信息的管理删改
2. 对路线信息的管理删改
3. 对公交、站点信息的管理删改
"""
import json
import datetime
from flask import Blueprint, request
from flask_cors import CORS
import op_db
from exts import db
from function.map import Get_lon_lat
from models import User, Admin, Route, Station, Bus

admin_server = Blueprint("admin", __name__)
CORS(admin_server, resources=r'/*')


@admin_server.route('/admin', methods=['GET', 'POST'])
def admin():
    admin_permit = request.values.get("admin_id")

    """选择何种操作则值为1"""
    # 删除用户信息
    dele_user = request.values.get("delete_user")

    # 站台信息
    edit_station = request.values.get("edit_station")
    dele_station = request.values.get("delete_station")
    add_station = request.values.get("add_station")

    # 路线信息
    edit_route = request.values.get("edit_route")
    dele_route = request.values.get("delete_route")
    add_route = request.values.get("add_route")

    # 公交信息
    edit_bus = request.values.get("edit_bus")
    dele_bus = request.values.get("delete_bus")
    add_bus = request.values.get("add_bus")

    if admin_permit:

        """
        ====================================
        删除用户信息
        ====================================
        """
        if dele_user == '1':
            # 获取要删除用户信息
            user_id_dele = request.values.get("user_id")
            if user_id_dele:
                # print(type(user_id_dele))
                d_user = User.query.filter(User.user_id == user_id_dele).first()
                me = Admin.query.filter(Admin.admin_id == admin_permit).first()
                me_id = me.user_id
                # print(type(me_id))
                if user_id_dele == str(me_id):  # 防止删除自己
                    res = {
                        "error_code": 400, "msg": "错误操作！您在删除自己！"
                    }
                elif d_user:
                    db.session.delete(d_user)
                    db.session.commit()
                    res = {
                        "error_code": 200, "msg": "删除成功！"
                    }
                else:
                    res = {
                        "error_code": 404, "msg": "删除失败！未找到该用户！"
                    }
            else:
                res = {
                    "error_code": 1001, "msg": "user_id未填!"
                }

            return json.dumps(res, ensure_ascii=False)  # 防止出现乱码

        """
        ====================================
        编辑路线信息
        ====================================
        """
        if edit_route == '1':
            route_id_edit = request.values.get("route_id")

            if route_id_edit:
                route_need = Route.query.filter(Route.route_id == route_id_edit).first()

                '''获取所需路线信息'''
                if request.method == 'GET':
                    if route_need:
                        route_need_name = route_need.route_name
                        res = {
                            "error_code": 200, "route_id": route_id_edit, "route_name": route_need_name
                        }
                        return json.dumps(res, ensure_ascii=False)
                    else:
                        res = {
                            "error_code": 404, "msg": "未查询到该路线信息！"
                        }
                        return json.dumps(res, ensure_ascii=False)

                '''修改所需路线信息'''
                if request.method == 'POST':
                    if route_need:
                        route_name_new = request.values.get("route_name")
                        route_need.route_name = route_name_new
                        db.session.commit()
                        res = {
                            "error_code": 200, "msg": "修改成功！"
                        }
                        return json.dumps(res, ensure_ascii=False)
                    else:
                        res = {
                            "error_code": 404, "msg": "未查询到该路线信息！"
                        }
                        return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "error_code": 1001, "msg": "route_id未填!"
                }
                return json.dumps(res, ensure_ascii=False)

        """
        ====================================
        删除路线信息
        ====================================
        """
        if dele_route == '1':
            route_name_dele = request.values.get("route_name")
            if route_name_dele:
                d_route = Route.query.filter(Route.route_name == route_name_dele).first()
                if d_route:
                    db.session.delete(d_route)
                    db.session.commit()
                    res = {
                        "error_code": 200, "msg": "删除成功！"
                    }
                else:
                    res = {
                        "error_code": 404, "msg": "删除失败！未找到该路线！"
                    }
            else:
                res = {
                    "error_code": 1001, "msg": "route_name未填!"
                }

            return json.dumps(res, ensure_ascii=False)  # 防止出现乱码

        """
        ===================================
        添加路线信息
        ===================================
        """
        if add_route == '1':
            new_route = request.values.get("route_name")
            if new_route:
                sql = "select* from route where route_name='%s';" % new_route  # 查看数据库中是否有这条路线，有的话说明重复
                result = op_db.login_add(sql)  # 执行sql
                if result:
                    res = {
                        "error_code": 1000, "msg": "路线已经存在!"
                    }
                else:
                    route_add = Route(route_name=new_route)
                    db.session.add(route_add)
                    db.session.commit()
                    route_find = Route.query.filter(Route.route_name == new_route).first()
                    route_id_return = route_find.route_id
                    res = {
                        "error_code": 200, "msg": "新增成功！", "route_id": route_id_return
                    }
                return json.dumps(res, ensure_ascii=False)

            else:
                res = {
                    "error_code": 1001, "msg": "route_name未填!"
                }
                return json.dumps(res, ensure_ascii=False)

        """
        =========================================
        编辑站点信息
        =========================================
        """
        if edit_station == '1':
            station_id_edit = request.values.get("station_id")
            if station_id_edit:
                station_need = Station.query.filter(Station.station_id == station_id_edit).first()

                if station_need:
                    station_need_name = station_need.station_name  # 站点名
                    station_need_type = station_need.station_type  # 站点类型（1）
                    station_need_lon = str(station_need.longitude)  # 站点经度
                    station_need_lat = str(station_need.latitude)  # 站点纬度

                    '''获取所需站点信息'''
                    if request.method == 'GET':
                        res = {
                            "error_code": 200, "station_name": station_need_name, "station_type": station_need_type,
                            "station_longitude": station_need_lon, "station_latitude": station_need_lat
                        }
                        return json.dumps(res, ensure_ascii=False)

                    '''修改所需站点信息'''
                    if request.method == 'POST':
                        station_name_edit = request.values.get("station_name")
                        if station_name_edit is None:
                            station_name_edit = station_need_name

                        station_type_edit = request.values.get("station_type")
                        if station_type_edit is None:
                            station_type_edit = station_need_type

                        station_lon_edit = request.values.get("station_longitude")
                        if station_lon_edit is None:
                            station_lon_edit = station_need_lon

                        station_lat_edit = request.values.get("station_latitude")
                        if station_lat_edit is None:
                            station_lat_edit = station_need_lat
                        station_need.station_name = station_name_edit
                        station_need.station_type = int(station_type_edit)
                        station_need.longitude = station_lon_edit
                        station_need.latitude = station_lat_edit
                        db.session.commit()
                        res = {
                            "error_code": 200, "msg": "修改成功！"
                        }
                        return json.dumps(res, ensure_ascii=False)
                else:
                    res = {
                        "error_code": 404, "msg": "未查询到该站点信息！"
                    }
                    return json.dumps(res, ensure_ascii=False)

            else:
                res = {
                    "error_code": 1001, "msg": "station_id未填!"
                }
                return json.dumps(res, ensure_ascii=False)

        """
        =======================================
        删除站点信息
        =======================================
        """
        if dele_station == '1':
            station_name_dele = request.values.get("station_name")
            if station_name_dele:
                d_station = Station.query.filter(Station.station_name == station_name_dele).first()
                if d_station:
                    db.session.delete(d_station)
                    db.session.commit()
                    res = {
                        "error_code": 200, "msg": "删除成功！"
                    }
                else:
                    res = {
                        "error_code": 404, "msg": "删除失败！未找到该站点！"
                    }
            else:
                res = {
                    "error_code": 1001, "msg": "station_name未填!"
                }

            return json.dumps(res, ensure_ascii=False)  # 防止出现乱码

        """
        ===========================================
        添加新的站点
        ===========================================
        """
        if add_station == '1':
            new_station_name = request.values.get("station_name")
            get_lon_lat = Get_lon_lat(new_station_name)
            new_station_type = int(request.values.get("station_type"))
            new_station_lon = get_lon_lat[0]
            new_station_lat = get_lon_lat[1]
            if new_station_name and new_station_type:
                sql = "select* from station where station_name='%s';" % new_station_name  # 查看数据库中是否有这个站点，有的话说明重复
                result = op_db.login_add(sql)  # 执行sql
                if result:
                    res = {
                        "error_code": 1000, "msg": "站点已经存在!"
                    }
                else:
                    station_add = Station(station_name=new_station_name, station_type=new_station_type, delete_type=0,
                                          longitude=new_station_lon, latitude=new_station_lat)
                    db.session.add(station_add)
                    db.session.commit()
                    station_find = Station.query.filter(Station.station_name == new_station_name).first()
                    station_id_return = station_find.station_id
                    res = {
                        "error_code": 200, "msg": "新增成功！", "station_id": station_id_return
                    }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "error_code": 1001, "msg": "station_name和station_type未填!"
                }
                return json.dumps(res, ensure_ascii=False)

        """
        ===========================================
        编辑公交信息
        ===========================================
        """
        if edit_bus == '1':
            bus_id_edit = request.values.get("bus_id")
            if bus_id_edit:
                bus_need = Bus.query.filter(Bus.bus_id == bus_id_edit).first()

                if bus_need:
                    bus_need_route = bus_need.route_id  # 路线ID
                    bus_need_user = bus_need.user_id  # 用户ID
                    bus_need_type = bus_need.type_id  # 公交类型（1）
                    bus_need_per = bus_need.permit_passengers  # 准载人数
                    bus_need_date = bus_need.start_date  # 开启日期
                    bus_need_bel = bus_need.belong_company  # 所属公司

                    '''获取所需公交信息'''
                    if request.method == 'GET':
                        res = {
                            "error_code": 200, "route_id": bus_need_route, "user_id": bus_need_user,
                            "type_id": bus_need_type, "permit_passengers": bus_need_per,
                            "start_date": str(bus_need_date), "belong_company": bus_need_bel
                        }
                        return json.dumps(res, ensure_ascii=False)

                    '''修改所需公交信息'''
                    if request.method == 'POST':
                        if bus_need:
                            bus_route_edit = request.values.get("route_id")
                            if bus_route_edit is None:
                                bus_route_edit = bus_need_route

                            bus_user_edit = request.values.get("user_id")
                            if bus_user_edit is None:
                                bus_user_edit = bus_need_user

                            bus_type_edit = request.values.get("type_id")
                            if bus_type_edit is None:
                                bus_type_edit = bus_need_type

                            bus_per_edit = request.values.get("permit_passengers")
                            if bus_per_edit is None:
                                bus_per_edit = bus_need_per

                            bus_date_edit = request.values.get("start_date")
                            if bus_date_edit is None:
                                bus_date_edit = str(bus_need_date)

                            bus_bel_edit = request.values.get("belong_company")
                            if bus_bel_edit is None:
                                bus_bel_edit = bus_need_bel

                            bus_need.route_id = int(bus_route_edit)
                            bus_need.user_id = int(bus_user_edit)
                            bus_need.type_id = int(bus_type_edit)
                            bus_need.permit_passengers = int(bus_per_edit)
                            bus_need.start_date = datetime.datetime.strptime(bus_date_edit, '%Y-%m-%d')
                            bus_need.belong_company = bus_bel_edit
                            db.session.commit()
                            res = {
                                "error_code": 200, "msg": "修改成功！"
                            }
                            return json.dumps(res, ensure_ascii=False)
                        else:
                            res = {
                                "error_code": 404, "msg": "未查询到该公交信息！"
                            }
                            return json.dumps(res, ensure_ascii=False)
                else:
                    res = {
                        "error_code": 404, "msg": "未查询到该公交信息！"
                    }
                    return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "error_code": 1001, "msg": "bus_id未填!"
                }
                return json.dumps(res, ensure_ascii=False)

        """
        ===========================================
        删除公交信息
        ===========================================
        """
        if dele_bus == '1':
            bus_id_dele = request.values.get("bus_id")
            if bus_id_dele:
                d_bus = Bus.query.filter(Bus.bus_id == bus_id_dele).first()
                if d_bus:
                    db.session.delete(d_bus)
                    db.session.commit()
                    res = {
                        "error_code": 200, "msg": "删除成功！"
                    }
                else:
                    res = {
                        "error_code": 404, "msg": "删除失败！未找到该公交！"
                    }
            else:
                res = {
                    "error_code": 1001, "msg": "bus_id未填!"
                }

            return json.dumps(res, ensure_ascii=False)  # 防止出现乱码

        """
        =====================================
        添加公交信息
        =====================================
        """
        if add_bus == '1':
            new_route_id = request.values.get("route_id")
            if new_route_id is None:
                new_route_id = 1

            new_user_id = int(request.values.get("user_id"))
            if new_user_id is None:
                new_user_id = 1

            new_type_id = request.values.get("type_id")
            new_per = request.values.get("permit_passengers")
            new_date_str = request.values.get("start_date")
            if new_date_str is None:
                new_date_str = '2020-01-01'

            new_bel = request.values.get("belong_company")
            if new_bel is None:
                new_bel = '天府通公交公司'

            if new_type_id and new_per:
                new_date = datetime.datetime.strptime(new_date_str, '%Y-%m-%d')
                bus_add = Bus(route_id=new_route_id, user_id=new_user_id, delete_type=0, type_id=new_type_id,
                              permit_passengers=new_per, start_date=new_date, belong_company=new_bel)
                db.session.add(bus_add)
                db.session.commit()
                sql = "select count(*) from bus"
                result = op_db.login_add(sql)
                bus_id_return = result[0].get('count(*)')
                # bus_find = Bus.query.filter(Bus.route_id == new_route_id).all()
                # bus_id_return = bus_find.bus_id
                res = {
                    "error_code": 200, "msg": "新增成功！", "bus_id": bus_id_return
                }
                return json.dumps(res, ensure_ascii=False)
            else:
                res = {
                    "error_code": 1001, "msg": "type_id或permit_passengers未填!"
                }
                return json.dumps(res, ensure_ascii=False)

        else:
            res = {
                "error_code": 404, "msg": "未选择操作类型！"
            }
            return json.dumps(res, ensure_ascii=False)

    else:
        res = {
            "error_code": 404, "msg": "管理员ID有误！"
        }
        return json.dumps(res, ensure_ascii=False)
