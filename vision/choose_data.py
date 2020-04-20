import pymysql
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

'''
sql_connect_bus_passenger()   单表查询 表bus_passenger
sql_connect_station_passenger()   单表查询 表station_passenger
choose_data_bus_passenger_info()   多表查询 表bus_passenger && 表passenger
choose_data_station_passenger_info()  多表查询 表station_passenger && 表passenger
'''



def sql_connect_bus_passenger():
    # 创建数据库连接
    db = pymysql.connect(host='123.57.55.107',
                         port=3306,
                         user='root',
                         passwd='Hello@world',
                         db='PopulationDensity',
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    try:
        # 编写SQL查询语句
        sql = "SELECT * FROM bus_passenger;"

        # 执行SQL查询语句
        cursor.execute(sql)
        # 获取查询的所有记录
        data_bus_passenger = cursor.fetchall()
        # 遍历结果
        # for row in data_bus_passenger:
        #     bus_id = row[1]
        #     passenger_id = row[2]
        #     timestamp = row[3]
        #     print(bus_id,passenger_id,timestamp)

        data_list = []
        for data in data_bus_passenger:
            item = {}
            # 表数据ID
            item["bus_passenger_id"] = data[0]
            # 公交车ID
            item["bus_id"] = data[1]
            # 乘客ID
            item["passenger_id"] = data[2]
            # 时间戳
            item["timestamp"] = data[3]

            data_list.append(item)

    except Exception as e:
        raise e
    finally:
        # 关闭连接
        cursor.close()
        db.close()
        return data_list


def sql_connect_station_passenger():
    # 创建数据库连接
    db = pymysql.connect(host='123.57.55.107',
                         port=3306,
                         user='root',
                         passwd='Hello@world',
                         db='PopulationDensity',
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    try:
        # 编写SQL查询语句
        sql = "SELECT * FROM station_passenger;"

        # 执行SQL查询语句
        cursor.execute(sql)
        # 获取查询的所有记录
        data_station_passenger = cursor.fetchall()
        # 遍历结果
        # for row in data_station_passenger:
        #     station_id = row[1]
        #     passenger_id = row[2]
        #     timestamp = row[3]
        #     print(station_id, passenger_id, timestamp)

        data_list = []
        for data in data_station_passenger:
            item = {}
            # 表数据ID
            item["station_passenger_id"] = data[0]
            # 站台ID
            item["station_id"] = data[1]
            # 乘客ID
            item["passenger_id"] = data[2]
            # 时间戳
            item["timestamp"] = data[3]

            data_list.append(item)

    except Exception as e:
        raise e
    finally:
        # 关闭连接
        cursor.close()
        db.close()
        return data_list


def choose_data_bus_passenger_info():
    # 创建数据库连接
    db = pymysql.connect(host='123.57.55.107',
                         port=3306,
                         user='root',
                         passwd='Hello@world',
                         db='PopulationDensity',
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    try:
        # 编写SQL查询语句
        sql = "select bus_passenger.*,passenger.* " \
              "from bus_passenger inner join passenger " \
              "on bus_passenger.passenger_id = passenger.passenger_id;"

        # 执行SQL查询语句
        cursor.execute(sql)
        # 获取查询的所有记录
        data_bus_passenger_info = cursor.fetchall()
        # 遍历结果
        for row in data_bus_passenger_info:
            bus_id = row[0]
            passenger_id = row[1]
            timestamp = row[2]
            sex = row[3]
            age_level = row[4]
            is_glasses = row[5]
            print(bus_id, passenger_id, timestamp,sex,age_level,is_glasses)

        data_list = []
        for data in data_bus_passenger_info:
            item = {}
            # 公交车ID
            item["bus_id"] = data[0]
            # 乘客ID
            item["passenger_id"] = data[1]
            # 时间戳
            item["timestamp"] = data[2]
            # 性别
            item["sex"] = data[3]
            # 年龄段
            item["age_level"] = data[4]
            # 是否佩戴眼镜
            item["is_glasses"] = data[5]
            # 是否佩戴帽子
            item["is_hat"] = data[6]
            # 是否佩戴口罩
            item["is_mask"] = data[7]
            # 是否涂口红
            item["is_lipstick"] = data[8]

            data_list.append(item)

        return data_list

    except Exception as e:
        raise e
    finally:
        # 关闭连接
        cursor.close()
        db.close()


def choose_data_station_passenger_info():
    '''
        处理mysql中的数据,提取有用的字段
        :return: list
    '''

    # 创建数据库连接
    db = pymysql.connect(host='123.57.55.107',
                         port=3306,
                         user='root',
                         passwd='Hello@world',
                         db='PopulationDensity',
                         charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    try:
        # 编写SQL查询语句
        sql = "select station_passenger.*,passenger.* " \
              "from station_passenger inner join passenger " \
              "on bus_passenger.passenger_id = passenger.passenger_id;"

        # 执行SQL查询语句
        cursor.execute(sql)
        # 获取查询的所有记录
        data_station_passenger_info = cursor.fetchall()
        # 遍历结果
        for row in data_station_passenger_info:
            station_id = row[0]
            passenger_id = row[1]
            timestamp = row[2]
            sex = row[3]
            age_level = row[4]
            is_glasses = row[5]
            print(station_id, passenger_id, timestamp, sex, age_level, is_glasses)

        data_list = []
        for data in data_station_passenger_info:
            item = {}
            # 站台ID
            item["station_id"] = data[0]
            # 乘客ID
            item["passenger_id"] = data[1]
            # 时间戳
            item["timestamp"] = data[2]
            # 性别
            item["sex"] = data[3]
            # 年龄段
            item["age_level"] = data[4]
            # 是否佩戴眼镜
            item["is_glasses"] = data[5]
            # 是否佩戴帽子
            item["is_hat"] = data[6]
            # 是否佩戴口罩
            item["is_mask"] = data[7]
            # 是否涂口红
            item["is_lipstick"] = data[8]

            data_list.append(item)

        return data_list

    except Exception as e:
        raise e
    finally:
        # 关闭连接
        cursor.close()
        db.close()


if __name__ == "__main__": 
    data1 = sql_connect_bus_passenger()
    print(data1)
    data2 = sql_connect_station_passenger()
    print(data2)