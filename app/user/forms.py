"""

File:forms.py
Author:wangduoyu
Date:2020-03-13
Connect:854429157@qq.com
Description:

"""
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Length


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名',validators=[Length(0,60)])
    location = StringField('用户住址',validators=[Length(0,60)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('更改资料')