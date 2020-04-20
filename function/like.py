# coding=utf-8
"""
站点收藏模块：
1. 用户登陆成功后可直接查看收藏的站点信息
2. 查看站点或公交信息时可将其进行收藏，在登录时即可直接推送
"""
from exts import db
from function.count_density import Count_bus, Count_station
from models import User_bus, User_station, Station
from sqlalchemy.sql import and_


def Add_like_bus(user_id_l, bus_id_l, timestamp):
    """收藏公交"""
    query_res = User_bus.query.filter(and_(User_bus.user_id == user_id_l, User_bus.bus_id == bus_id_l)).first()
    # 检查是否重复收藏
    if query_res:
        res = "收藏公交信息重复！"
        return res
    else:
        add_b = User_bus(user_id=user_id_l, bus_id=bus_id_l, timestamp=timestamp)
        db.session.add(add_b)
        db.session.commit()
        res = "收藏公交信息成功！"
        return res


def Add_like_station(user_id_l, station_id_l, timestamp):
    """收藏站点"""
    query_res = User_station.query.filter(and_(User_station.user_id == user_id_l,
                                               User_station.station_id == station_id_l)).first()
    # print(station_id_l)
    # 检查是否重复收藏
    if query_res:
        res = "收藏站点信息重复！"
        return res
    else:
        add_s = User_station(user_id=user_id_l, station_id=station_id_l, timestamp=timestamp)
        db.session.add(add_s)
        db.session.commit()
        res = "收藏站点信息成功！"
        return res


def Show_like_bus(user_id_l, timestamp):
    """展示收藏公交"""
    show_b = User_bus.query.filter(User_bus.user_id == user_id_l).all()
    res_list = []
    if show_b:
        print(show_b)
        for b in show_b:
            id = b.bus_id
            dens = Count_bus(timestamp_log=timestamp, bus_id_log=id)
            res = {
                "bus_id": id, "density": dens
            }
            res_list.append(res)
        return res_list
    else:
        res = "您尚未收藏任何公交信息！"
        return res


def Show_like_station(user_id_l, timestamp):
    """展示收藏站点"""
    show_s = User_station.query.filter(User_station.user_id == user_id_l).all()
    res_list = []
    if show_s:
        print(show_s)
        for s in show_s:
            id = s.station_id
            s_info = Station.query.filter(Station.station_id == id).first()
            s_name = s_info.station_name
            dens = Count_station(timestamp_log=timestamp, station_id_log=id)
            res = {
                "station_name": s_name, "density": dens
            }
            res_list.append(res)
        return res_list
    else:
        res = "您尚未收藏任何站点信息！"
        return res


# if __name__ == '__main__':
#     Show_like_bus(2)

