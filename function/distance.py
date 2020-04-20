"""
公式计算两点间距离（m）
"""

from math import radians, cos, sin, asin, sqrt, fabs
from models import Station
import op_db


# def geodistance(lng1, lat1, lng2, lat2):
#     lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])  # 经纬度转换成弧度
#     dlon = lng2-lng1
#     dlat = lat2-lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     distance = 2*asin(sqrt(a))*6371*1000  # 地球平均半径，6371km
#     distance_last = round(distance/1000, 3)
#     return distance_last

EARTH_RADIUS = 6371  # 地球平均半径，6371km


def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance_hav(lat0, lng0, lat1, lng1):
    """用haversine公式计算球面两点间的距离。"""
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))
    d = int(distance)

    return d


def min_station(lon_m, lat_m):
    sql = "SELECT COUNT(*) FROM station;"
    result = op_db.login_add(sql)  # 执行sql
    length = result[0].get('COUNT(*)')
    i = 1
    min = 6371000  # 地球平均半径，6371km
    id = 0
    while i <= length:
        station = Station.query.filter(Station.station_id == i).first()
        lon = station.longitude
        lat = station.latitude
        dis = get_distance_hav(lng0=lon, lat0=lat, lng1=lon_m, lat1=lat_m)
        if min >= dis:
            min = dis
            id = i
        i += 1
    station_need = Station.query.filter(Station.station_id == id).first()
    station_name = station_need.station_name
    return station_name

