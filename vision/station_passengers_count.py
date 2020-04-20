# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from vision.choose_data import sql_connect_station_passenger
from vision.data_format import get_data_frame,str_datetime_frame
import matplotlib.font_manager as fm
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from io import BytesIO
from lxml import etree
import base64
import plotly.graph_objects as go
import plotly.offline as pltoff

'''
实现功能:展示某号站台的人群数量随时间的变化情况折线图
调用函数：show_station_passengers_count_ply(station_id,start_date,end_date)
'''

#设置字体
myfont = fm.FontProperties(fname="./vision/AdobeHeitiStd-Regular.otf")

def station_passengers_count_(station_id,start_date,end_date):
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
    # 选择某号站台的乘客
    new_df = new_df[new_df["station_id"] == station_id]
    # 选择起始时间之后的数据
    start_date = str_datetime_frame(start_date)
    new_df = new_df[new_df["timestamp"] >= start_date]
    # 选择结束时间之前的数据
    end_date = str_datetime_frame(end_date)
    new_df = new_df[new_df["timestamp"] <= end_date]
    # 设置timestamp为索引
    new_df = new_df.set_index("timestamp")
    # 只选择据中的count列
    new_df = new_df["count"]
    # 调整统计时间的范围,实现重新采样
    new_df = new_df.resample("10T").sum()
    # print(new_df)
    return new_df

def show_station_passengers_count_mpl(station_id,start_date,end_date):
    df = station_passengers_count_(station_id,start_date,end_date)
    df = pd.DataFrame(df, columns=["count"])
    fig = plt.figure(figsize=(16, 8))
    ax = plt.subplot()
    _x = range(len(df.index))
    _y = df["count"]

    # 绘制折线图,效果不明显
    # ax.plot(_x, _y,)
    # ax.plot(_x, _y,alpha=0.5,color='#EE7600')
    # 绘制竖着的直方图
    ax.bar(_x, _y, width=0.5, align="center", color='#EE7600')

    # 解决xticklable时间带年月日
    xticklables = [i.strftime('%H:%M') for i in df.index]
    # 解决xticklable刻度太密集
    # plt.xticks(range(0, len(df.index), 4), xticklables[::4], rotation=45)
    plt.xticks(range(0, len(df.index)), xticklables, rotation=45)
    # x轴标题
    plt.xlabel("时间", fontproperties=myfont)
    # y轴标题
    plt.ylabel("数量", fontproperties=myfont)
    # 图的标题
    # plt.title("2号站台在这一天各时刻的人群数量统计直方图", fontproperties=myfont)
    # plt.savefig("2号站台在这一天各时刻的人群数量统计直方图.jpg")
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
    iris_im = """<h1>2号站台在这一天各时刻的人群数量统计直方图</h1>  """ + """<img src="%s">""" % imd

    root = "<title>Iris Dataset</title>"
    root = root  + iris_im  # 将多个 html 格式的字符串连接起来

    # lxml 库的 etree 解析字符串为 html 代码，并写入文件
    html = etree.HTML(root)
    tree = etree.ElementTree(html)
    tree.write('某站台在这一天各时刻的人群数量统计直方图.html')

    # 最后使用默认浏览器打开 html 文件
    import webbrowser
    webbrowser.open('某站台在这一天各时刻的人群数量统计直方图.html', new=1)

def show_station_passengers_count_ply(station_id,start_date,end_date):
    '''
    展示某号站台的人群数量随时间的变化情况折线图
    :param station_id: 站台ID int类型  2
    :param start_date: 起始时间 str类型  "2020-04-05 00:00:00"
    :param end_date: 结束时间 str类型  "2020-04-06 00:00:00"
    :return: str类型 将生成的HTML通过字符串的形式返回
    '''
    df = station_passengers_count_(station_id,start_date,end_date)
    df = pd.DataFrame(df, columns=["count"])

    _x = df.index
    _y = df["count"]
    # print(_x,_y)

    fig = go.Figure()
    # 绘制折线图
    fig.add_trace(go.Scatter(x=_x, y=_y, name='Station '+str(station_id),
                             line=dict(color='firebrick', width=4)))
    # 设置图表布局
    fig.update_layout(title=str(station_id) + '号站台的人群数量随时间的变化情况折线图',
                      title_font_size=40,
                      xaxis=dict(title='时间',  # 设置坐标轴的标签
                                 titlefont=dict(size=30),  # 设置坐标轴标签的字体大小
                                 tickfont=dict(size=24),  # 设置刻度的字体大小
                                 ),
                      yaxis=dict(title='数量',  # 设置坐标轴的标签
                                 titlefont=dict(size=30),  # 设置坐标轴标签的字体大小
                                 tickfont=dict(size=24),  # 设置刻度的字体大小
                                 ),
                      )
    # 使用离线的接口，生成离线html
    # pltoff.plot(fig, filename=str(station_id)+"号站台的人群数量随时间的变化情况.html")
    # 将生成的HTML通过字符串的形式返回
    plt_res = pltoff.plot(fig, output_type='div')
    # print(plt_res)
    # with open("res.html",'w+') as f:
    #     f.write(plt_res)
    return plt_res


if __name__ == '__main__':
    # show_station_passengers_count_mpl(2,"2020-04-05 00:00:00","2020-04-06 00:00:00")
    show_station_passengers_count_ply(2, "2020-04-06 00:00:00","2020-04-07 00:00:00")