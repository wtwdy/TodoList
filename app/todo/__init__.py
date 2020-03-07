"""

File:__init__.py.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
# 1.创建蓝图

from flask import Blueprint

todo = Blueprint('todo',__name__)

from app.todo import views