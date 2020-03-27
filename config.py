"""

File:config.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
"""
存储配置
"""

import os

# 获取当前项目的绝对路径
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    所有配置环境的基类,包含通用配置
    """
    # 尤其是设计(Flask-WTF)登录注册里面提交敏感信息时,一定要加
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'westos secret key'
    # 是否自动提交修改
    # flask-sqlchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 是否跟踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PER_PAGE = 2



    # 邮件前缀
    FLASK_MAIL_SUBJECT_PREFIX ='[TodoList]'
    # 邮件发送者
    FLASK_MAIL_SENDER = 'wangtuo1115@163.com'



class DevelopmentConfig(Config):
    """
    开发环境的配置信息
    """
    # 启用了调试支持,服务器会在代码修改后自动重新加载,并在发生错误时提供一个相当有用的调试器
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    # MAIL_USE_TLS = True
    # os.environ.get: 先从os.environ环境中寻找是否存在MAIL_USERNAME变量，如果存在直接拿出，不存在则赋值为wangtuo1115
    MAIL_USERNAME = 'wangtuo1115'
    MAIL_PASSWORD = 'wang85429157'
    # 数据库提交地址
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')






    # 启用了调试支持,服务器会在代码修改后自动重新载入,并在发生错误时提供一个相当有用的调试器。
    # DEBUG = True
    # """
    # QQ邮箱:  MAIL_PORT=465 MAIL_USE_SSL=True
    # 163邮箱: MAIL_PORT=25  MAIL_USE_SSL=False(默认不开启)
    # """
    # MAIL_SERVER = 'smtp.163.com'  # 邮件服务器
    # MAIL_PORT = 25  # 邮件服务器的端口
    # # MAIL_USE_SSL = True
    # MAIL_USERNAME = 'wangtuo1115@163.com'  # 发送者邮箱账户
    # MAIL_PASSWORD = 'wang85429157'  # 授权密码而不是登录密码
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
   """
  测试环境的配置信息
  """
   TESTING = True
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
   """
  生产环境的配置信息,生产环境debug一定要关闭
  """
   DEBUG = False
   MAIL_SERVER = 'smtp.163.com'
   MAIL_PORT = 25
   # MAIL_USE_TLS = True
   # os.environ.get: 先从os.environ环境中寻找是否存在MAIL_USERNAME变量，如果存在直接拿出，不存在则赋值为wangtuo1115
   MAIL_USERNAME = 'wangtuo1115'
   MAIL_PASSWORD = 'wang85429157'
   # 数据库提交地址
   SQLALCHEMY_DATABASE_URI = 'mysql://flask:westos@175.24.105.189/todolist'


# 不同的环境对应不同的名字
config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig,

}