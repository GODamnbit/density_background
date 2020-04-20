# coding=utf-8
"""
登录模块：
1. 输入个人ID和密码进行登录操作
2. 分权限身份登录（管理员和普通用户）
3. 向用户推荐“离我最近”的站点
4. 向用户推荐收藏的公交或是站点
"""
import json
from flask import request, Blueprint
import op_db
from flask_cors import *
from function.count_density import Count_station
from function.distance import min_station
from exts import db
from function.like import Show_like_bus, Show_like_station
from function.map import Map
from models import User, Station, Admin

log_server = Blueprint('login', __name__)
CORS(log_server, resources=r'/*')


@log_server.route('/login', methods=['GET'])
def login():
    # 登录需要两个参数，user_id和pwd
    user_id_log = request.values.get('user_id')
    passwd_log = request.values.get('password')
    lon_log = request.values.get('longitude')
    lat_log = request.values.get('latitude')
    timestamp = request.values.get('timestamp')
    role = request.values.get('role')  # 1为管理员，0为普通用户

    if role == '1':
        # 管理员登录
        if user_id_log and passwd_log:  # 非空为真
            # 需要先写一个导入数据库的函数
            sql = "SELECT * FROM user WHERE user_id='%s' AND password='%s';" % (user_id_log, passwd_log)
            result = op_db.login_add(sql)  # 执行sql
            if result:
                user = User.query.filter(User.user_id == user_id_log).first()
                show_like_bus = Show_like_bus(user_id_l=user_id_log, timestamp=timestamp)  # 展示收藏公交信息
                show_like_station = Show_like_station(user_id_l=user_id_log, timestamp=timestamp)  # 展示收藏站点信息
                head_image = user.head_img
                if head_image is None:
                    head_image = "https://gw.alipayobjects.com/zos/rmsportal/MRhHctKOineMbKAZslML.jpg"
                admin = Admin.query.filter(Admin.user_id == user_id_log).first()
                if admin:
                    admin_id = admin.admin_id
                    if lon_log and lat_log:
                        """根据用户当前经纬度位置进行推送"""
                        user.longitude = lon_log
                        user.latitude = lat_log
                        db.session.commit()
                        station_name = min_station(lon_m=lon_log, lat_m=lat_log)
                        station = Station.query.filter(Station.station_name == station_name).first()
                        station_id = station.station_id
                        nearest_density = Count_station(timestamp_log=timestamp, station_id_log=station_id)
                        # 接口返回的都是json
                        res = {
                            "error_code": 1000, "msg": "登录成功!", "admin_id": admin_id,
                            "head_img": head_image, "station_name": station_name, "nearest_density": nearest_density
                            # , "like_bus_density": show_like_bus, "like_station_density": show_like_station
                        }
                    else:
                        res = {
                            "error_code": 1001, "msg": "登录成功!但无法获取您的位置。", "admin_id": admin_id,
                            "head_img": head_image
                            # , "like_bus_density": show_like_bus, "like_station_density": show_like_station
                        }
                else:
                    res = {
                        "error_code": 404, "msg": "抱歉您不是管理员！"
                    }
            else:
                res = {
                    "error_code": 3001, "msg": "账号或密码错误！"
                }
        else:
            res = {
                "error_code": 3000, "msg": "必填参数未填，请查看接口文档！"
            }

        return json.dumps(res, ensure_ascii=False)  # 防止出现乱码；json.dumps()函数是将字典转化为字符串

    if role == '0':
        # 普通用户登录
        if user_id_log and passwd_log:  # 非空为真
            # 需要先写一个导入数据库的函数
            sql = "SELECT * FROM user WHERE user_id='%s' AND password='%s';" % (user_id_log, passwd_log)
            result = op_db.login_add(sql)  # 执行sql
            if result:
                user = User.query.filter(User.user_id == user_id_log).first()
                # show_like_bus = Show_like_bus(user_id_l=user_id_log, timestamp=timestamp)  # 展示收藏公交信息
                # show_like_station = Show_like_station(user_id_l=user_id_log, timestamp=timestamp)  # 展示收藏站点信息
                head_image = user.head_img
                if head_image is None:
                    head_image = "https://gw.alipayobjects.com/zos/rmsportal/MRhHctKOineMbKAZslML.jpg"
                if lon_log and lat_log:
                    """根据用户当前经纬度位置进行推送"""
                    user.longitude = lon_log
                    user.latitude = lat_log
                    db.session.commit()
                    print(float(lon_log))
                    print(float(lat_log))
                    station_name = min_station(lon_m=float(lon_log), lat_m=float(lat_log))
                    station = Station.query.filter(Station.station_name == station_name).first()
                    station_id = station.station_id
                    s_lon = station.longitude
                    s_lat = station.latitude
                    map_img = Map(lon=s_lon, lat=s_lat, st_name=station_name, my_lon=lon_log, my_lat=lat_log)
                    nearest_density = Count_station(timestamp_log=timestamp, station_id_log=station_id)
                    # 接口返回的都是json
                    res = {
                        "error_code": 1000, "msg": "登录成功!", "head_img": head_image, "station_name": station_name,
                        "nearest_density": nearest_density, "map_img": map_img
                        # , "like_bus_density": show_like_bus, "like_station_density": show_like_station
                    }
                else:
                    res = {
                        "error_code": 1001, "msg": "登录成功!但无法获取您的位置。", "head_img": head_image
                        # , "like_bus_density": show_like_bus, "like_station_density": show_like_station
                    }
            else:
                res = {
                    "error_code": 3001, "msg": "账号或密码错误！"
                }
        else:
            res = {
                "error_code": 3000, "msg": "必填参数未填，请查看接口文档！"
            }

        return json.dumps(res, ensure_ascii=False)  # 防止出现乱码；json.dumps()函数是将字典转化为字符串

    if role is None:
        # 未选择登录身份
        res = {
            "error_code": 404, "msg": "未选择登录身份！"
        }
        return json.dumps(res, ensure_ascii=False)

