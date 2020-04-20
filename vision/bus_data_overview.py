# coding=utf-8
import json

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from vision.choose_data import sql_connect_bus_passenger
from vision.data_format import get_data_frame,str_datetime_frame
import matplotlib.font_manager as fm
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from io import BytesIO
from lxml import etree
import base64
import plotly.offline as pltoff
import plotly.graph_objs as go

'''
统计分析主题
to管理员
1.不同公交路线的人群数量随时间的变化情况  函数所在py文件名：bus_data_overview
2.不同站台的人群数量随时间的变化情况  station_data_overview
to用户
3.某路公交车上人群数量随时间的变化情况  bus_passengers_count  
4.某号站台的人群数量随时间的变化情况  station_passengers_count
5.某段时间内不同站台的人群数量统计情况  different_station_count
'''

'''
实现功能:展示不同公交路线的人群数量随时间的变化情况折线图
调用函数：show_bus_date_overview_ply(start_date, end_date)
'''

#设置字体
myfont = fm.FontProperties(fname="C:\Windows\Fonts\AdobeHeitiStd-Regular.otf")

def show_bus_date_overview_mpl(start_date,end_date):
    global temp_grouped
    fig = plt.figure(figsize=(16, 8))
    ax = plt.subplot()
    #获取数据
    df = get_data_frame(sql_connect_bus_passenger())
    df = df[["bus_id", "passenger_id", "timestamp"]]
    #为现存的每条数据作出统计,即让其数量为1,方便之后分组后的聚合
    count_df = pd.DataFrame(np.ones(shape=(len(df),1)),columns=["count"])
    df = df.join(count_df)
    #去除没有时间戳的乘客
    new_df = df[pd.notnull(df["timestamp"])]

    # 选择起始时间之后的数据
    start_date = str_datetime_frame(start_date)
    new_df = new_df[new_df["timestamp"] >= start_date]
    # 选择结束时间之后的数据
    end_date = str_datetime_frame(end_date)
    new_df = new_df[new_df["timestamp"] <= end_date]

    #不同公交路线的乘客的数量和时间的对应关系并不相同,需要先统一统计的时间,没有的时间段填充0
    date_start = new_df["timestamp"].min()
    date_end = new_df["timestamp"].max()
    date_period = pd.DataFrame(pd.date_range(date_start, date_end, freq="T",),columns=["timestamp"])

    #定义绘图的颜色
    colors = ['red', 'green', 'blue', "cyan", "orange"]
    bus_list = new_df["bus_id"].unique().tolist()
    #分组
    for bus,grouped in new_df.groupby(by=["bus_id"]):
        #对不同的站台添加统一的时间段,并设置为index
        temp_grouped = grouped.merge(date_period,how="outer",on="timestamp")
        temp_grouped = temp_grouped[["timestamp","count"]].set_index("timestamp")
        #对空白的时间段填充0
        temp_grouped = temp_grouped.fillna(0)
        temp_grouped = temp_grouped.resample("10T").sum()
        # print(temp_grouped.index)
        _x = range(len(temp_grouped.index))
        _y = temp_grouped["count"]
        #绘制散点图,但是效果不明显
        # ax.scatter(_x, _y,
        #            c=colors[bus_list.index(bus)],
        #            alpha=0.5,
        #            label=bus
        #            )
        #绘制折线图
        ax.plot(_x, _y,
                   c=colors[bus_list.index(bus)],
                   alpha=0.5,
                   label=bus
                   )
        # 解决xticklable时间带时分秒
        xticklables = [i.strftime('%Y-%m') for i in temp_grouped.index]
        # 解决xticklable刻度太密集
        plt.xticks(range(0, len(temp_grouped.index), 4), xticklables[::4], rotation=45)

    #添加图例
    plt.legend()
    # x轴标题
    plt.xlabel("时间",fontproperties=myfont)
    # y轴标题
    plt.ylabel("时间段内的数量合计",fontproperties=myfont)
    # 图的标题
    # plt.title("不同公交线路的人群数量随时间的变化情况",fontproperties=myfont)
    # plt.savefig("不同公交线路的人群数量随时间的变化情况.png")
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
    iris_im = """<h1>不同公交线路的人群数量随时间的变化情况折线图</h1>  """ + """<img src="%s">""" % imd

    root = "<title>Iris Dataset</title>"
    root = root + iris_im  # 将多个 html 格式的字符串连接起来

    # lxml 库的 etree 解析字符串为 html 代码，并写入文件
    html = etree.HTML(root)
    tree = etree.ElementTree(html)
    tree.write('不同公交线路的人群数量随时间的变化情况折线图.html')

    # 最后使用默认浏览器打开 html 文件
    import webbrowser
    webbrowser.open('不同公交线路的人群数量随时间的变化情况折线图.html', new=1)


def show_bus_date_overview_ply(start_date, end_date):
    '''
    展示不同公交路线的人群数量随时间的变化情况折线图
    :param start_date: 起始时间 str类型  "2020-04-06 00:00:00"
    :param end_date: 结束时间 str类型  "2020-04-07 00:00:00"
    :return: str类型 将生成的HTML通过字符串的形式返回
    '''
    global temp_grouped
    fig = go.Figure()
    # 获取数据
    df = get_data_frame(sql_connect_bus_passenger())
    df = df[["bus_id", "passenger_id", "timestamp"]]
    # 为现存的每条数据作出统计,即让其数量为1,方便之后分组后的聚合
    count_df = pd.DataFrame(np.ones(shape=(len(df), 1)), columns=["count"])
    df = df.join(count_df)
    # 去除没有时间戳的乘客
    new_df = df[pd.notnull(df["timestamp"])]

    # 选择起始时间之后的数据
    start_date = str_datetime_frame(start_date)
    new_df = new_df[new_df["timestamp"] >= start_date]
    # 选择结束时间之后的数据
    end_date = str_datetime_frame(end_date)
    new_df = new_df[new_df["timestamp"] <= end_date]

    # 不同公交线路的乘客的数量和时间的对应关系并不相同,需要先统一统计的时间,没有的时间段填充0
    date_start = new_df["timestamp"].min()
    date_end = new_df["timestamp"].max()
    date_period = pd.DataFrame(pd.date_range(date_start, date_end, freq="T", ), columns=["timestamp"])

    # 定义绘图的颜色
    colors = ['red', 'green', 'blue', "cyan", "orange"]
    bus_list = new_df["bus_id"].unique().tolist()
    # 分组
    for bus, grouped in new_df.groupby(by=["bus_id"]):
        # 对不同的公交线路添加统一的时间段,并设置为index
        temp_grouped = grouped.merge(date_period, how="outer", on="timestamp")
        temp_grouped = temp_grouped[["timestamp", "count"]].set_index("timestamp")
        # 对空白的时间段填充0
        temp_grouped = temp_grouped.fillna(0)
        temp_grouped = temp_grouped.resample("10T").sum()
        # print(temp_grouped.index)
        _x = temp_grouped.index
        _y = temp_grouped["count"]

        # 绘制折线图
        fig.add_trace(go.Scatter(x=_x, y=_y,
                                 name=bus,
                                 mode='lines+markers',
                                 line=dict(color=colors[bus_list.index(bus)], width=4)))

    # 设置图表布局
    fig.update_layout(title='不同公交线路的人群数量随时间的变化情况折线图',
                      title_font_size=40,
                      xaxis=dict(title='时间',  # 设置坐标轴的标签
                                 titlefont=dict(size=30),  # 设置坐标轴标签的字体大小
                                 tickfont=dict(size=24),  # 设置刻度的字体大小
                                 ),
                      yaxis=dict(title='时间段内的数量合计',  # 设置坐标轴的标签
                                 titlefont=dict(size=30),  # 设置坐标轴标签的字体大小
                                 tickfont=dict(size=24),  # 设置刻度的字体大小
                                 ),
                      )
    # 使用离线的接口，生成离线html
    # pltoff.plot(fig, filename="不同公交线路的人群数量随时间的变化情况折线图.html")
    # 将生成的HTML通过字符串的形式返回
    plt_res = pltoff.plot(fig, output_type='div')
    # print(plt_res)
    # with open("res.html",'w+') as f:
    #      f.write(plt_res)
    return plt_res


if __name__ == '__main__':
    date = "2020-04-06 15:32:00"
    start = "2020-04-06 00:00:00"
    end = "2020-04-07 00:00:00"
    # show_bus_date_overview_mpl(start,end)
    show_bus_date_overview_ply(start,end)
