# coding=utf-8
"""
注册模块：
1. 个人电话号码，用户名，电子邮箱，密码，（删除类型），性别，头像，住址，生日，（经纬度），介绍
2. 用户ID由系统自动分配
3. 电话号码，用户名，密码，性别，生日不可为空
"""
import json
import op_db
from flask import Blueprint, request
from models import User
from flask_cors import *
from exts import db
import re


add_server = Blueprint('add', __name__)
CORS(add_server, resources=r'/*')


@add_server.route('/add', methods=['POST'])
def add():
    # user_id_log = request.values.get("user_id")
    phone = request.values.get("phone")
    user_name = request.values.get("user_name")
    password = request.values.get("password")
    if_re = re.search(r"\W", phone)
    if phone and user_name and password:  # 必填参数校验
        sql = "select* from user where phone='%s';" % phone  # 查看数据库中是否有这个手机号，有的话说明重复
        result = op_db.login_add(sql)  # 执行sql
        if result:
            res = {
                "error_code": 1000, "msg": "电话号已经存在!"
            }
        elif phone.isspace or if_re or len(phone) < 11:
            res = {
                "error_code": 1001, "msg": "电话号格式不正确!"
            }
        else:
            # sql = "INSERT INTO user(user_id, phone, user_name, email, password, sex, born_date)" \
            #       "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
            #       % (user_id_log, phone, user_name, email, password, sex, birth)
            # op_db.login_add(sql)
            user_add = User(phone=phone, user_name=user_name, email='null', password=password, delete_type=0,
                            sex=1, head_img='null', address='null', born_date='1999-1-1', longitude=0,
                            latitude=0, production='null')
            db.session.add(user_add)
            db.session.commit()
            user_find = User.query.filter(User.phone == phone).first()
            user_id_return = user_find.user_id
            res = {
                "error_code": 200, "msg": "新增成功！", "user_id": user_id_return
            }
    else:
        res = {
            "error_code": 3007, "msg": "必填参数未填写!"
        }
    return json.dumps(res, ensure_ascii=False)  # 防止出现乱码
