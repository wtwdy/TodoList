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
from app.models import Role, User

app = create_app()
# 0.0.0.0代表任意
# 绑定本机的所有ip，http://IP:8888
# app.run(host='0.0.0.0',port=8888)
manager = Manager(app)
migrate = Migrate(app,db)

@manager.command
def tests():
    """run the unit tests"""
    import unittest
    # 发现所有的测试用例(TestCase)绑定成一个测试集合(TestSuit),--->TestLoader
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
# from app.auth import views

if __name__ == '__main__':

    def make_shell_context():
        return dict(app=app,db=db,Role=Role,User=User)

    manager.add_command('shell',Shell(make_context=make_shell_context))
    manager.add_command('db',MigrateCommand)
    manager.run()
