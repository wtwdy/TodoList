"""

File:models.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
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

class User(db.Model):
    """用户"""
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password_hash = db.Column(db.String(200))
    email = db.Column(db.String(20))
    # 外键关联

    role_id = db.Column(db.Integer(),db.ForeignKey('roles.id'))

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