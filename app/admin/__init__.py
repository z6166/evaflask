# -*- coding=utf-8 -*-
from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views, errors
'''
前面我们载入了一个名为admin的蓝图模块
在这里我们需要构建这个模块
'''