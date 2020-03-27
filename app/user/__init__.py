"""

File:__init__.py.py
Author:wangduoyu
Date:2020-03-13
Connect:854429157@qq.com
Description:

"""
from flask import Blueprint

# 创建蓝图
user = Blueprint('user',__name__)

from . import views