"""

File:01_proprety属性.py
Author:wangduoyu
Date:2020-03-08
Connect:854429157@qq.com
Description:

"""
class Good(object):
    def __init__(self,name,price):
        self.name = name
        self.__price = price

    @property # 将类方法编程类属性
    def price(self):
        return self.__price

    @price.setter
    def price(self,value):
        self.__price = value

if __name__ == '__main__':
    good = Good('python book', 100)
    print(good.price)
    good.price = 1000
    print(good.price)