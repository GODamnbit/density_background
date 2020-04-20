# coding=utf-8
from flask_script import Manager
from flask_migrate import Migrate
from app import app
from exts import db

manager = Manager(app)
Migrate(app, db)


if __name__ == '__main__':
    manager.run()
