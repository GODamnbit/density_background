# coding=utf-8
import json

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from vision.choose_data import sql_connect_station_passenger
from vision.data_format import get_data_frame,str_datetime_frame,normaltime
import matplotlib.font_manager as fm
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from io import BytesIO
from lxml import etree
import base64
import plotly.offline as pltoff
import plotly.graph_objs as go

'''
实现功能:展示某段时间内不同站台的人群数量统计直方图
调用函数：show_different_station_count_ply(start_date,end_date)
'''

#设置字体
myfont = fm.FontProperties(fname="./vision/AdobeHeitiStd-Regular.otf")

def different_station_count_(start_date,end_date):
    # 获取数据
    df = get_data_frame(sql_connect_station_passenger())
    # 只选择数据中所需的列
    df = df[["station_id", "passenger_id", "timestamp"]]
    # 为现存的每条数据作出统计,即让其数量为1,方便之后分组后的聚合
    count_df = pd.DataFrame(np.ones(shape=(len(df), 1)), columns=["count"])
    df = df.join(count_df)
    # 去除没有station_id的乘客
    new_df = df[pd.notnull(df["station_id"])]
    # 去除没有时间戳的乘客
    new_df = new_df[pd.notnull(df["timestamp"])]
    # 选择起始时间之后的数据
    start_date = str_datetime_frame(start_date)
    new_df = new_df[new_df["timestamp"] >= start_date]
    # 选择结束时间之前的数据
    end_date = str_datetime_frame(end_date)
    new_df = new_df[new_df["timestamp"] <= end_date]
    # 获取站台列表
    # station_list = new_df["station_id"].unique().tolist()
    # 设置station_id为索引
    new_df = new_df.set_index("station_id")
    # 只选择据中的count列
    new_df = new_df["count"]
    # 根据站台分组,并且进行求和
    new_df = new_df.groupby("station_id").sum()
    print(new_df)
    return new_df

def show_different_station_count_mpl(start_date,end_date):
    df = different_station_count_(start_date,end_date)
    df = pd.DataFrame(df, columns=["count"])
    figure = plt.figure(figsize=(10, 8))
    ax = plt.subplot()
    _x = range(len(df.index))
    _y = df["count"]

    # 画竖着的直方图
    # ax.bar(_x, _y, width=0.5, align="center",color='#EE7600')
    # plt.xticks(range(0, len(df.index)), df.index, fontproperties=myfont)
    # 画横着的直方图
    ax.barh(_x, _y, align="center", color='#EE7600', ecolor='black')

    # 设置y轴值
    plt.yticks(range(0, len(df.index)), df.index, fontproperties=myfont)
    # y轴标题
    plt.ylabel("站台", fontproperties=myfont)
    # x轴标题
    plt.xlabel("数量", fontproperties=myfont)
    # 图的标题
    # plt.title("某时刻不同站台的人群数量统计", fontproperties=myfont)
    # plt.savefig("某时刻不同站台的人群数量统计.jpg")
    # plt.show()

    # 将生成的matplotlib图像转化为HTML格式
    # figure 保存为二进制文件
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()

    # 图像数据转化为 HTML 格式
    imb = base64.b64encode(plot_data)
    # imb = plot_data.encode('base64')   # 对于 Python 2.7可用
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    iris_im = """<h1>某时刻各站台的人群数量统计直方图</h1>  """ + """<img src="%s">""" % imd

    root = "<title>Iris Dataset</title>"
    root = root + iris_im  # 将多个 html 格式的字符串连接起来

    # lxml 库的 etree 解析字符串为 html 代码，并写入文件
    html = etree.HTML(root)
    tree = etree.ElementTree(html)
    tree.write('某时刻各站台的人群数量统计直方图.html')

    # 最后使用默认浏览器打开 html 文件
    import webbrowser
    webbrowser.open('某时刻各站台的人群数量统计直方图.html', new=1)


def show_different_station_count_ply(start_date,end_date):
    '''
    展示某段时间内不同站台的人群数量统计直方图
    :param start_date: 起始时间 str类型  "2020-04-05 00:00:00"
    :param end_date: 结束时间 str类型  "2020-04-06 00:00:00"
    :return: str类型 将生成的HTML通过字符串的形式返回
    '''
    global _x,_y
    df = different_station_count_(start_date,end_date)
    df = pd.DataFrame(df, columns=["count"])
    # 获取站台列表
    # station_list = df.index.unique().tolist()
    # print(station_list)
    # for i in station_list:
    #     _x = ['station ' + str(i)]

    # _x = df.index
    _x = ['Station 1','Station 2']
    _y = df["count"]
    # print(_x,_y)

    fig = go.Figure()
    # 绘制条形图
    fig = go.Figure(data=[go.Bar(
        x=_x, y=_y,
        text=_y,
        # textposition='auto',  #数字显示在柱形内
        textposition='outside'  #数字显示在柱形外
    )])
    # 设置图表布局
    fig.update_layout(title="该时段内各个站台的人群数量统计直方图",
                      title_font_size=40,
                      xaxis=dict(title='站台',
                                 titlefont=dict(size=30),
                                 tickfont=dict(size=24),
                                 ),
                      yaxis=dict(title='数量',  # 设置坐标轴的标签
                                 titlefont=dict(size=30),  # 设置坐标轴标签的字体及颜色
                                 tickfont=dict(size=24),  # 设置刻度的字体大小及颜色
                                 ),
                      )
    #使用离线的接口，生成离线html
    # pltoff.plot(fig, filename="该时段内各个站台的人群数量统计直方图.html")
    # 将生成的HTML通过字符串的形式返回
    plt_res = pltoff.plot(fig, output_type='div')
    # print(plt_res)
    # with open("res.html",'w+') as f:
    #     f.write(plt_res)
    return plt_res


if __name__ == '__main__':
    date = "2020-04-06 15:26:00"
    start = "2020-04-06 00:00:00"
    end = "2020-04-11 00:00:00"
    # show_different_station_count_mpl(date)
    show_different_station_count_ply(start,end)