"""

File:forms.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError

from app.models import User


class RegisterationForm(FlaskForm):
    email = StringField('电子邮箱', validators=
    [DataRequired(),
     Length(1, 100),
     Email()],
                        render_kw={
                            'class': 'ayui-input',
                            'placeholder': '电子邮箱'
                        })

    username = StringField('用户名', validators=
    [DataRequired(),
     Length(1, 100),
     # ^:以什么开头,$：以什么结尾,\w代表单个字母数字或者下划线，*代表前一个字符出现0次或者多次
     Regexp('^\w*$', message='用户名必须由数字字母和下划线组成')],
                           render_kw={
                               'class': 'ayui-input',
                               'placeholder': '用户名'
                           })

    password = PasswordField('密码', validators=[
        DataRequired()],
                             render_kw={
                                 'class': 'ayui-input',
                                 'placeholder': '密码'
                             })
    repassword = PasswordField('确认密码', validators=[
        DataRequired(),
        EqualTo('password', message='密码不一致')],
                               render_kw={
                                   'class': 'ayui-input',
                                   'placeholder': '确认密码'
                               })

    submit = SubmitField('注册')

    # 两个自定义的验证函数,以validate_开头且跟着字段名的方法,这个方法和常规的验证函数一起调用
    # field自动传入
    def validate_email(self, field):
        # field是email表单对象,field.data时email表单提交的数据
        # select * from users where email='xxx' limit 1;
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("邮箱地址%s已经注册！" % (field.data))

    def validate_username(self, field):
        # field是username表单对象,field.data时username表单提交的数据
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名%s已经注册！" % (field.data))


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[
        DataRequired(), Email(), Length(1, 100)],
                        render_kw={
                            'class': 'ayui-input',
                            'placeholder': '电子邮箱'
                        })
    password = PasswordField('密码', validators=[
        DataRequired(), Length(1, 100)],
                             render_kw={
                                 'class': 'ayui-input',
                                 'placeholder': '密码'
                             })

    submit = SubmitField('登录')
