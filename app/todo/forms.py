"""

File:forms.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField
from wtforms.validators import DataRequired

from app.models import Category


class AddTodoForm(FlaskForm):
    content = StringField(label='任务内容',
                          validators=[DataRequired()],
                          render_kw={
                            'class' :"form-control",
                            'placeholder':"Add Todo"
                          })
    category = SelectField(label='任务类型',
                           coerce=int,
                           render_kw={
                            'class' : "btn btn-default dropdown-toggle"
                           }) #存的是id整形
                           # choice=[(item.id,item.name for item in Category.query.all()),


    submit = SubmitField(label='添加任务',
                         render_kw={
                            'class' : "btn btn-default btn-todo-add"
                         })

    # 目的：每次实例化新的对象时,都会重新遍历任务分类的表单,确保新写的任务分类添加了进来
    def __init__(self):
        # 执行父类的构造方法
        super(AddTodoForm,self).__init__()
        categories = Category.query.all()
        if categories:
            self.category.choices = [(item.id, item.name) for item in
categories]
        else:
            self.category.choices = [(-1,'请先创建分类')]

class EditTodoForm(FlaskForm):
    content = StringField(label='任务内容',
                          validators=[DataRequired()])

    category = SelectField(label='任务类型',
                           coerce=int)
    submit = SubmitField('编辑任务')

    def __init__(self):
        super(EditTodoForm,self).__init__()
        categories = Category.query.all()
        if categories:
            self.category.choices = [(item.id,item.name) for item in categories]
        else:
            self.category.choices = [-1,"请先创建任务分类"]