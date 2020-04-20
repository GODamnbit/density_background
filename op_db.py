# coding=utf-8
import pymysql


def login_add(sql):
    conn = pymysql.connect(
        host='123.57.55.107',
        user='root',
        password='Hello@world',
        db='PopulationDensity',
        charset='utf8',
        autocommit=True  # 自动提交

    )
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 建立游标；默认返回二维数组，DictCursor指定返回字典；
    cur.execute(sql)  # execute帮你执行sql
    res = cur.fetchall()  # 拿到全部sql执行结果
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库
    return res  # 返回sql执行的结果


def fabu(sql):
    conn = pymysql.connect(
        host='123.57.55.107',
        user='root',
        password='Hello@world',
        db='PopulationDensity',
        charset='utf8',
        autocommit=True  # 自动提交

    )
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 建立游标；默认返回二维数组，DictCursor指定返回字典；
    cur.execute(sql)  # execute帮你执行sql
    res = cur.fetchone()  # 拿到全部sql执行结果
    cur.close()  # 关闭游标
    conn.close()  # 关闭数据库
    return res  # 返回sql执行的结果
