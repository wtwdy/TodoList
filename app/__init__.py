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


from config import config

"""
程序工厂函数,延迟创建程序实例
"""



bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()

def create_app(config_name = 'development'):
    """
    默认创建开发环境的app
    :param config_name:
    :return:
    """
    app = Flask(__name__)
    """
    config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
    """
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    # from app.auth import views
    # 3.注册蓝图,和app关联在一块
    from app.auth import auth
    from app.todo import todo
    app.register_blueprint(auth,url_prefix='/auth')
    app.register_blueprint(todo)
    return app

