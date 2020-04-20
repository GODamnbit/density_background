# coding=utf-8
"""
index模块

"""

from flask import Flask
from fabu import station_fabu, bus_fabu
from user import edit_user, login, add, admin
import config
import station_vision
from exts import db
from flask_cors import *


# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(config)  # 配置文件实例化
#     app.register_blueprint(login.log_server)
#     app.register_blueprint(add.add_server)
#     app.register_blueprint(fabu.fa)
#     app.register_blueprint(delete_user.delete_server)
#     db.init_app(app)
#     return app
#
#
# app = create_app()
# CORS(app, resources=r'/*')

app = Flask(__name__)
app.config.from_object(config)  # 配置文件实例化
app.register_blueprint(login.log_server)  # 登录模块蓝图注册
app.register_blueprint(add.add_server)  # 注册模块蓝图注册
app.register_blueprint(station_fabu.station_server)  # 站台查询模块蓝图注册
app.register_blueprint(edit_user.edit_user_server)  # 个人中心模块蓝图注册
app.register_blueprint(station_vision.vision_server)  # 可视化模块蓝图注册
app.register_blueprint(bus_fabu.bus_server)  # 公交查询模块蓝图注册
app.register_blueprint(admin.admin_server)  # 管理员模块蓝图注册
db.init_app(app)
CORS(app, resources=r'/*')


@app.route('/')
def index():
    return '这是首页！'


if __name__ == '__main__':
    # app = create_app()
    app.run(host='0.0.0.0', debug=True)
