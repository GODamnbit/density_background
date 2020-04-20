# coding=utf-8
"""
个人信息编辑模块：
1. 个人电话号码，用户名，电子邮箱，密码，（删除类型），性别，头像，住址，生日，（经纬度），介绍
2. 用户ID由系统自动分配
3. 电话号码，用户名，密码，性别，生日不可为空
"""
import json
# import re
import op_db
from flask import Blueprint, request
from models import User
from flask_cors import *
from exts import db

edit_user_server = Blueprint('edit_user', __name__)
CORS(edit_user_server, resources=r'/*')


@edit_user_server.route('/edit', methods=['GET', 'POST'])
def edit():
    user_id_return = request.values.get("user_id")
    user_info = User.query.filter(User.user_id == user_id_return).first()

    """获取当前个人信息"""
    phone_this = user_info.phone
    user_name_this = user_info.user_name
    password_this = user_info.password
    email_this = user_info.email
    sex_this = user_info.sex
    if sex_this == 1:
        sex_this = '男'
    else:
        sex_this = '女'
    head_img_this = user_info.head_img
    if head_img_this is None:
        head_img_this = 'https://gw.alipayobjects.com/zos/rmsportal/MRhHctKOineMbKAZslML.jpg'
    address_this = user_info.address
    birth_this = user_info.born_date
    longitude_this = str(user_info.longitude)
    if longitude_this is None:
        longitude_this = 'null'
    latitude_this = str(user_info.latitude)
    if latitude_this is None:
        latitude_this = 'null'
    production_this = user_info.production

    if request.method == 'GET':
        res = {"error_code": 200, "phone": phone_this, "user_name": user_name_this, "password": password_this,
               "email": email_this, "sex": sex_this, "head_img": head_img_this, "address": address_this,
               "birth": str(birth_this), "longitude": longitude_this, "latitude": latitude_this,
               "production": production_this}

        return json.dumps(res, ensure_ascii=False)

    if request.method == 'POST':
        """提交修改后的个人信息"""
        phone_new = request.values.get("phone")
        if phone_new is None:
            phone_new = phone_this

        user_name_new = request.values.get("user_name")
        if user_name_new is None:
            user_name_new = user_name_this

        password_new = request.values.get("password")
        if password_new is None:
            password_new = password_this

        email_new = request.values.get("email")
        if email_new is None:
            email_new = email_this

        sex_new = request.values.get("sex")
        if sex_new:
            if sex_new == '男':
                sex_new = 1
            elif sex_new == '女':
                sex_new = 0
        else:
            sex_new = 1

        head_img_new = request.form["head_img"]
        if head_img_new is None:
            head_img_new = head_img_new

        address_new = request.values.get("address")
        if address_new is None:
            address_new = address_this

        birth_new = request.values.get("born_date")
        if birth_new is None:
            birth_new = birth_this

        longitude_new = request.values.get("longitude")
        if longitude_new is None:
            longitude_new = 0

        latitude_new = request.values.get("latitude")
        if latitude_new is None:
            latitude_new = 0

        production_new = request.values.get("production")
        if production_new is None:
            production_new = production_this

        sql = "select* from user where phone='%s';" % phone_new  # 查看数据库中是否有这个手机号，有的话说明重复
        result = op_db.login_add(sql)  # 执行sql
        # if_re = re.search(r"\W", phone_new)
        if result:
            res = {"error_code": 1000, "msg": "电话号已经存在!"}
        elif len(phone_new) < 11 or len(phone_new) > 12:
            # 是否有空格、特殊符号、长度是否为11位
            res = {"error_code": 1001, "msg": "电话号格式不正确!"}
        else:
            user_info.phone = phone_new
            user_info.user_name = user_name_new
            user_info.password = password_new
            user_info.email = email_new
            user_info.sex = sex_new
            user_info.head_img = head_img_new
            user_info.address = address_new
            user_info.born_date = birth_new
            user_info.longitude = longitude_new
            user_info.latitude = latitude_new
            user_info.production = production_new
            db.session.commit()
            res = {
                "error_code": 200, "msg": "修改成功！"
            }

        return json.dumps(res, ensure_ascii=False)  # 防止出现乱码
