"""

File:__init__.py.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
# 1.创建蓝图
from flask import Blueprint
# 'auth'蓝图名称,__name__:蓝图存放位置
auth = Blueprint('auth',__name__)

from . import views

