"""

File:models.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
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
    confirmed = db.Column(db.Boolean,default=False)

    # 外键关联
    role_id = db.Column(db.Integer(),db.ForeignKey('roles.id'))

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

# login_manager回调函数的作用：
#     注册回调函数,当没有session_id时,通过装饰器指定的函数来读取用户到session中，达到用户可通过current_user获取当前登录的用户

# 加载用户的回调函数;如果能找到用户,返回用户对象;否则返回 None 。
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))