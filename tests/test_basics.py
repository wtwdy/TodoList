"""

File:test_basics.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""
import unittest

# 获取当前正在运行的app
from flask import current_app

from app import create_app

class BasicsTestCase(unittest.TestCase):
    """
    setUp()和tearDown()方法分别在各测试前后执行,并且测试用例是以test_开头的作为测试执行
    """
    def setUp(self):
        """
        在测试之前创建一个测试环境
            1). 使用测试配置创建程序
            2). 激活上下文,确保能在测试中使用current_app
            3). 创建一个全新的数据库,以备不时之需
        :return:
        """
        # 创建测试模块
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        # 将app与上下文绑定到一起
        self.app_context.push()

    def tearDown(self):
        # 将app与上下文断开
        self.app_context.pop()

    def test_app_exists(self):
        """
        测试当前app是否存在
        :return:
        """
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """
        测试当前app是否为测试环境
        :return:
        """
        self.assertTrue(current_app.config['TESTING'])