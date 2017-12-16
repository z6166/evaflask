# -*- coding=utf-8 -*-
from app import create_app, db
from flask_script import Manager, Shell
from app.models import Record
from flask_migrate import Migrate, MigrateCommand   # 载入migrate扩展


app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)  # 注册migrate到flask

manager.add_command('db', MigrateCommand)   #在终端环境下添加一个db命令


if __name__ == '__main__':
    manager.run()
