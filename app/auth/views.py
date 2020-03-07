"""

File:views.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
# 2.应用蓝图
from app.auth import auth

@auth.route('/')
def index():
    return 'index'

@auth.route('/login/')
def login():
    return 'login'

@auth.route('/logout/')
def logout():
    return 'logout'
@auth.route('/register/')
def register():
    return 'register'