"""

File:views.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
# 2.应用蓝图
from flask_login import login_user, login_required, logout_user

from app import db
from app.auth import auth
from app.auth.forms import RegisterationForm,LoginForm
from flask import render_template, flash, redirect, url_for,session

from app.models import User, Role


@auth.route('/')
def index():
    return render_template('auth/index.html')
    # return 'index'

@auth.route('/login/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # 调用Flask_Login中的login_user()函数,在用户会话中把用户标记为已登录
            login_user(user)
            flash("用户%s登录成功" %(user.username),category='success')
            return redirect(url_for('auth.index'))
        else:
            flash("用户登录失败", category='error')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html',form=form)
    # return 'login'

@auth.route('/logout/')
# 注销的前提是用户登录,login_required判断用户是否登录
@login_required
def logout():
    logout_user()
    flash("用户注销成功",category='success')
    return redirect(url_for('auth.index'))

@auth.route('/register/',methods=['GET','POST'])
def register():
    """
    /register:
        -GET:获取注册页面
        -POST：获取注册页面提交的数据
            1). 判断是否为POST方法提交数据,并且数据是否通过表单验证
            2). 如果通过验证,将表单提交的数据存储到数据库中,注册成功跳转到登录页面
        获取表单提交的数据有两种方式：
            <1>: form.data('email')
            <2>: form.email.data
    :return:
    """

    form = RegisterationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        # user.role = Role.query.filter_by(name='普通会员').first()
        db.session.add(user)
        flash("用户%s注册成功" %(user.username),category='success')

        # print(form.data)   #获取表单中提交的所有信息,以字典方式存储
        # print(form.password.data)
        # print(form.username.data)
        # print(form.email.data)

        # return redirect('/login')
        # url_for('auth.login')根据视图函数寻找对应的路由地址,/login
        return redirect(url_for('auth.login'))

    return render_template('/auth/register.html',form=form)

    # return 'register'