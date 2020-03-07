"""

File:test_number.py
Author:wangduoyu
Date:2020-03-07
Connect:854429157@qq.com
Description:

"""

import random
import unittest

class TestSequenceFunctions(unittest.TestCase):
    """
    setUp()和tearDown()分别在各测试前后执行,并且名字一test_开头的函数都作为测试执行
    """
    def setUp(self):
        self.seq = [1, 2, 3, 4, 5, 6]

    def test_choice_ok(self):
        """测试choice方法"""
        item = random.choice(self.seq)
        result = item in self.seq
        self.assertTrue(result)

    def test_sample_ok(self):
        """测试sample方法"""
        result = random.sample(self.seq,4)
        self.assertEqual(len(result),4)

    def tearDown(self):
        del self.seq
