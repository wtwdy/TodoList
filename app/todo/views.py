"""

File:views.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""

# 2.应用蓝图

from app.todo import todo

@todo.route('/')
def index():
    return 'index'


@todo.route('/login/')
def login():
    return 'login'

@todo.route('/logout/')
def logout():
    return 'logout'