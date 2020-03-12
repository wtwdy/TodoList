"""

File:views.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""

# 2.应用蓝图

from app.todo import todo

@todo.route('/add/')
def add():
    return 'todo add'


@todo.route('/delete/')
def delete():
    return 'todo delete'

