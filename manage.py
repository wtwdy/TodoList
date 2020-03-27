"""

File:manage.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
from flask_script import Manager, Shell
from flask_migrate import Migrate,MigrateCommand
from  app import create_app,db
from app.models import Role, User, Category, Todo

app = create_app(config_name='production')
# 0.0.0.0代表开放本机所有IP
# 绑定本机的所有ip，http://IP:8888
# app.run(host='0.0.0.0',port=8888)
manager = Manager(app)
# 将数据库迁移插件与数据库db和app关联起来
migrate = Migrate(app,db)

@manager.command
def tests():
    """run the unit tests 执行Flask项目的测试用例 """
    import unittest
    # 发现所有的测试用例(TestCase)绑定成一个测试集合(TestSuit),--->TestLoader
    # 将tests目录下的所有测试用例绑定成一个测试集合
    tests = unittest.TestLoader().discover('tests')
    # verbosity=2：测试结果会显示每个测试用例的所有相关信息，复杂度有0,1,2
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def category_init():
    """初始化分类信息"""
    ca1 = Category(name='重要紧急任务')
    ca2 = Category(name='不重要紧急任务')
    ca3 = Category(name='重要不紧急任务')
    ca4 = Category(name='不重要不紧急任务')
    db.session.add_all([ca1,ca2,ca3,ca4])
    db.session.commit()


# from app.auth import views

# 初始化Flask-Script。Flask-Migrate和为Python shell定义的上下文
# 当交互式环境python3 manager.py shell ,自动传入参数/变量：app,db,Role,User
def make_shell_context():
    return dict(app=app,db=db,Role=Role,User=User, Category=Category, Todo=Todo)


# def make_shell_context():
#     return dict(app=app,name='westos',age=10)

manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':

    manager.run()
