"""

File:__init__.py.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import pymysql

pymysql.install_as_MySQLdb()


from config import config

"""
程序工厂函数的目的： 延迟创建Flask应用,应用场景如下：
    1).测试，可以使用多个应用程序的实例，为每个实例分配不同的配置,从而测试每一种不同的情况
    2).多个实例.要同时运行同一个应用的不同版本,可以再你的web服务器中配置多个实例并分配不同的配置

"""



bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
# session_protection 属性提供不同的安全等级防止用户会话篡改
login_manager.session_protection = 'strong'
# login_view 属性设置登录页面的端点
login_manager.login_view='auth.login'

def create_app(config_name = 'development'):
    """
    默认创建开发环境的app
    :param config_name:
    :return:
    """
    # 实例化Flask对象
    app = Flask(__name__)
    """
    config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
    """
    # 关联配置信息
    app.config.from_object(config[config_name])
    # 实例化app对象,将配置信息和app关联起来
    # config[config_name].init_app(app)
    # 将bootstrap,mail,db 与app关联起来
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


    # from app.auth import views
    # 3.注册蓝图,和app关联在一块
    # 导包时导入的是__init__文件,没有将views.py导入，这里需要将views.py导入
    from app.auth import auth
    # url_prefix='/auth' 访问时前缀为/auth
    app.register_blueprint(auth)

    from app.user import user
    # 注册user蓝图
    app.register_blueprint(user)


    from app.todo import todo
    # 访问时不需要前缀,无前缀时为todo
    app.register_blueprint(todo,url_prefix='/todo')

    return app

