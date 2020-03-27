"""

File:models.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
from datetime import datetime

"""
数据库操作
"""
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from app import db
from itsdangerous import TimedJSONWebSignatureSerializer


# 数据库对应关系一对多时,将外键写在多的那一方
# 用户类型：用户---> 1:N

# Flask中的一个Model子类就是数据库中的一个表.默认表名为类名的小写,Role.lower()--->role
class Role(db.Model):
    """用户类型"""
    __tablename__ = 'roles' # 自定义的表名
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    # 作了两件事,1). Role添加属性users, 2).User添加role属性
    users = db.relationship('User',backref='role')

    def __repr__(self):
        return "<Role: %s>" %(self.name)


"""
Flask-Login 提供了一个 UserMixin 类,包含常用方法的默认实现,且能满足大多数需求。

        1). is_authenticated    用户是否已经登录?  
        2). is_active           是否允许用户登录?False代表用户禁用
        3). is_anonymous        是否匿名用户?
        4). get_id()            返回用户的唯一标识符
数据库对应关系：
 User：Role = N：1
 User：Todo = 1 : N
 User：Category = 1:N
 Todo:Category = N:1
"""

class User(UserMixin,db.Model):
    """用户"""
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password_hash = db.Column(db.String(200))
    email = db.Column(db.String(20),unique=True,index=True)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(20))
    confirmed = db.Column(db.Boolean,default=False)   # 账户是否已经确认
    name = db.Column(db.String(60)) # 用户真实姓名
    location = db.Column(db.String(60))  # 所在地
    about_me = db.Column(db.Text())  # 自我介绍

    # 注册日期
    #   default参数可以接收函数作为默认值
    #   所以每次生成默认值时,db.Column()都会调用指定的函数
    create_time = db.Column(db.DateTime(),default=datetime.utcnow)

    #最后访问日期
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)

    def ping(self):
        """刷新用户最后访问的时间"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # 外键关联
    role_id = db.Column(db.Integer(),db.ForeignKey('roles.id'))

    # 反向引用： 1). User添加属性todos,2).Todo添加属性user
    todos = db.relationship('Todo',backref='user')
    # 反向引用： 1). User添加属性category,2).Category添加属性user
    category = db.relationship('Category',backref='user')

    def generate_confirmation_token(self,expiration=3600):
        """生成一个令牌,有效期默认为1小时"""
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self,token):
        """检验令牌和检查令牌中的id和已登录用户id是否匹配？如果通过检验,则把新添加的confirmed属性设置为True"""
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except Exception as e:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed =  True
        db.session.add(self)
        db.session.commit()
        return True


    def __repr__(self):
        return "<User: %s>" %(self.username)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        # generate_password_hash(password, method= pbkdf2:sha1 , salt_length=8):密码加密的散列值。
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        # check_password_hash(hash, password) :密码散列值和用户输入的密码是否匹配.
        return check_password_hash(self.password_hash,password)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True) #任务id
    content = db.Column(db.String(100)) # 任务内容
    status = db.Column(db.Boolean,default=False) #任务状态
    add_time = db.Column(db.DateTime,default=datetime.utcnow) #任务创建时间
    # User:Todo =1:N
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    # Category:Todo = 1:N
    category_id = db.Column(db.Integer,db.ForeignKey('categories.id'))

    def __repr__(self):
        return "<Todo: %s>" %(self.content)

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    name = db.Column(db.String(60),unique=True)
    add_time = db.Column(db.DateTime,default=datetime.utcnow) #任务创建时间
    # User:Category=1:N
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    #反向引用
    todos = db.relationship('Todo',backref='category')

    def __repr__(self):
        return '<Category: %s>' %(self.name)




# login_manager回调函数的作用：
#     注册回调函数,当没有session_id时,通过装饰器指定的函数来读取用户到session中，达到用户可通过current_user获取当前登录的用户

# 加载用户的回调函数;如果能找到用户,返回用户对象;否则返回 None 。
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))


