"""

File:views.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
# 2.应用蓝图
from flask_login import login_user, login_required, logout_user, current_user

from app import db
from app.auth import auth
from app.auth.forms import RegisterationForm,LoginForm
from flask import render_template, flash, redirect, url_for, request

from app.email import send_mail
# from app.auth.send_mail import send_mail
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
            return redirect(url_for('todo.list'))
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
        # 提交数据库之后才能赋予新用户 id 值,而确认令牌需要用到 id ,所以不能延后提交。
        # db.session.commit()
        flash("用户%s注册成功" %(user.username),category='success')
        user.ping()   # 更新用户最后一次登录时间
        # 生成用户密文
        token = user.generate_confirmation_token()
        print(user.email,token)
        # 接收人以列表方式存储
        send_mail(to=[user.email], subject='请激活你的任务管理平台帐号',
                  filename='auth/confirm', user=user, token=token)

        flash("平台验证消息已经发送到你的邮箱,请确认后登录.",category='success')


        # print(form.data)   #获取表单中提交的所有信息,以字典方式存储
        # print(form.password.data)
        # print(form.username.data)
        # print(form.email.data)

        # return redirect('/login')
        # url_for('auth.login')根据视图函数寻找对应的路由地址,/login
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html',form=form)

    # return 'register'

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    1. 判断账户是否通过验证,如果通过验证,跳转到主页
    2. 如果没有验证,执行验证函数,更新账户的confirmed值
    """
    if current_user.confirmed:
        return redirect(url_for('todo.list'))
    if current_user.confirm(token):
        flash("验证邮箱通过",category='success')
        return redirect(url_for('todo.list'))
    else:
        flash('验证连接失败',category='error')
        return redirect(url_for('todo.login'))


@auth.before_app_request
def before_request():
    # 当前用户已经登录,没有被确认,请求的端点不在auth中,不是静态文件时,跳转到unconfirmed页面
    # 也就是说访问auth中的login,register,logout...或者static静态文件时不会被拦截
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed/')
def unconfirmed():
    # 如果当前用户是匿名用户或者已经验证的用户,则访问主页,否则进入未验证的界面
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('todo.list'))
    token = current_user.generate_confirmation_token()
    return render_template('auth/unconfirmed.html',token=token)

@auth.route('/reconfirm/')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    try:
        send_mail(to=[current_user.email], subject='请激活你的任务管理平台帐号',
                  filename='auth/confirm', user=current_user, token=token)
    except Exception as e:
        flash(str(e),category='error')
        return redirect(url_for('auth.register'))
    else:
        flash('新的平台验证信息已经发送至你的邮箱,请确认后登录',category='success')
        return redirect(url_for('todo.index'))