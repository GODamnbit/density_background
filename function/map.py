# coding=utf-8
"""
地图服务：
基于百度地图进行地图展示
"""
import json
from urllib.parse import quote
from urllib.request import urlopen


def Map(lon, lat, st_name, my_lon, my_lat):
    """获取百度地图静态图并标志"""
    map = "http://api.map.baidu.com/staticimage/v2?ak=AjbHqBlLrhoM6qNj49gcqwxa2Cvq2bqU&width=500&height=300" \
          "&center=" + str(my_lon) + "," + str(my_lat) + "&markers=" + str(my_lon) + "," + str(my_lat) + \
          "&markerStyles=l,M,0xff0000&labels=" + str(lon) + "," + str(lat) \
          + "&zoom=14&labelStyles=%s,1,14,0xffffff,0x000fff,1" % st_name

    return map


def Get_lon_lat(sta_name):
    """获取指定站点的经纬度"""
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = 'AjbHqBlLrhoM6qNj49gcqwxa2Cvq2bqU'
    address = quote(sta_name)
    uri = url + '?' + 'address=' + address + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode()
    temp = json.loads(res)
    lat = temp['result']['location']['lat']
    lng = temp['result']['location']['lng']
    return lng, lat


# if __name__ == '__main__':
#     Map(lon="104.086146", lat="30.659682", st_name="春熙路地铁站", my_lon="104.087", my_lat="30.658")
#     Get_lon_lat(sta_name="成都市春熙路")
