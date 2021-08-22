#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/21 21:13
# @Author : Henry
from unittest import TestCase
import unittest

# 使用type 去创建用例类
MyTest = type('MyTest', (TestCase, ), {'cases:': [1, 2, 3],
                                       'test_1': lambda x: x,
                                       'test_2': lambda x: x})

# suite = unittest.defaultTestLoader.loadTestsFromTestCase(MyTest)
# unittest.main()
# 自定义元类来实现动态创建测试类和测试方法
# 什么时候需要用到元类：
#     1. 动态创建类，在创建类的过程中要自定义类属性和方法


class MyMateClass(type):

    def __new__(cls, name, bases, attr, *args, **kwargs):
        # 通过元类创建一个类
        test_cls = super(MyMateClass, cls).__new__(cls, name, bases, attr)
        # 遍历属性Cases
        for index, case in enumerate(attr['Cases']):
            # 动态给test_cls这个类添加方法
            setattr(test_cls, 'test_{}'.format(index), lambda x: x)
        return test_cls


    pass


class BaseApiCase:
    """用例执行的基类"""

    def test_perform(self, case):
        """用例执行方法"""
        print('test cases:', case)
        # 1. 用例数据的处理
        # 2. 接口请求
        # 3. 响应数据提取
        # 4. 断言
        pass


my = MyMateClass('Henry', (unittest.TestCase, BaseApiCase),
                 {'Cases': [1, 2, 33]})
print(my)
