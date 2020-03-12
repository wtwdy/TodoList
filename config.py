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
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 是否跟踪修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 邮件前缀
    FLASK_MAIL_SUBJECT_PREFIX ='[TodoList]'
    # 邮件发送者
    FLASK_MAIL_SENDER = 'wangtuo1115@163.com'

    @staticmethod # 静态方法
    # 修饰第三方模块
    # 初始化app,用来添加第三方插件
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """
    开发环境的配置信息
    """
    # 启用了调试支持,服务器会在代码修改后自动重新加载,并在发生错误时提供一个相当有用的调试器
    DEBUG = True
    MAIL_SERVER = 'stmp.163.com'
    MAIL_PORT = 25
    # MAIL_USE_TLS = True
    # os.environ.get: 先从os.environ环境中寻找是否存在MAIL_USERNAME变量，如果存在直接拿出，不存在则赋值为wangtuo1115
    MAIL_USENAME = os.environ.get('MAIL_USERNAME') or 'wangtuo1115'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '密码'
    # 数据库提交地址
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data-dev.sqlite')

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
   SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,
'data.sqlite')

# 不同的环境对应不同的名字
config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}