#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/21 21:13
# @Author : Henry
from unittest import TestCase
import unittest
import yaml
import json
from datetime import datetime


# 面向对象 - 封装 继承 多态（伪多态，对数据类型没有严格限制）
class A:
    a_value = 1
    attr = 10

    def func_a(self):
        print('func_a')

    def work(self):
        print('work in A')


class B:
    b_value = 9
    attr = 90

    def work(self):
        print('work in B')


class Demo(A, B):

    @property  # 定义只读属性
    def b_attr(self):
        return B.attr  # 获取B中的attr属性


d = Demo()
# 调用父类的属性或方法
print(d.b_value)
d.func_a()
# 调用两个父类的同名方法和属性
print(d.attr)  # attr继承自A - 先继承A，则使用A的属性或方法 - 就近原则
d.work()  # 继承自A
print(d.b_attr)  # 只读属性

# 复习
"""
# 多态：python中函数的参数是没有类型限制的，所以多态在python中的体现不是很严谨。多态的概念是应用于java，c#这一类强类型语言中，而python
# 崇尚‘鸭子类型’
# 鸭子类型概念： 它并不要求严格的继承体系，关注的不是对象的类型本身，而是它是否具有要调用的方法（行为）
# 鸭子类型在python中的案例
    # 内置函数iter: 参数可以是实现迭代协议__iter__方法的任意类型对象
    # 函数len(): 调用对象的__len__魔术方法
"""


# 多继承的应用
# 定义一个api测试的用例类
#     1. 用例数据的数据
#     2. 接口请求
#     3. 响应数据提取
#     4. 断言


class HandleData:
    """用例数据的数据处理类"""
    def handle_data(self):
        pass


class RequestApi:
    """接口请求处理类"""

    def request_api(self):
        pass


# 基类case继承以上类，便于后续维护管理
class BaseTest(HandleData, RequestApi):
    pass


# 元类
class MyPython:
    pass


m = MyPython()

print(type(m))  # <class '__main__.MyPython'>
print(type(MyPython))  # <class 'type'> 通过type所创建的对象
print(type('string'))
print(type([11, 22]))
print(type(dict))  # <class 'type'>
print(type(str))
print(type(list))

# python中所有的类的类型都是type， type就是元类，创建类的类

# 使用type 去创建用例类
"""
type(object_or_name, bases, dict)
type(object) -> the object's type
type(name, bases, dict) -> a new type
type 动态创建类：
    参数1：name 类名 （字符串类型）
    参数2：bases 继承的父类 （元组类型）
    参数3：dict 类的属性和方法 （字典类型）
"""

# 通过type定义的类, 元类一般用不到
MyNew = type('MyNew', (object,), {'name': 'henry'})
print(MyNew)  # <class '__main__.TypeTest'> 等同于 class MyNew定义类
print(MyNew.__dict__)

# 通过type动态生成测试类
# test_1, test_2 unittest用的测试方法，无法写测试方法逻辑
# MyTest = type('MyTest', (TestCase, ), {'cases:': [1, 2, 3],
#                                        'test_1': lambda x: x,
#                                        'test_2': lambda x: x})

# suite = unittest.defaultTestLoader.loadTestsFromTestCase(MyTest)
# unittest.main()
"""====自定义元类来实现动态创建测试类和测试方法===="""


# 生成测试类的时候，根据测试数据去动态生成测试方法
# 什么时候需要用到元类： 动态创建类，在创建类的过程中需要自定义类属性和方法
# 需求： 自定义元类来动态创建测试类和测试方法


def test_value(funny, value):
    def inner(self, *args, **kwargs):
        result = funny(self, value, *args, **kwargs)
        return result

    return inner
    pass


# 继承元类type , class type(object) type 继承了object
class MyMateClass(type):

    # 通过类创建对象 第一参数cls 推荐写成mcs
    def __new__(mcs, name, bases, attr, *args, **kwargs):
        # 通过元类创建一个类， 调用父类的方法
        test_cls = super(MyMateClass, mcs).__new__(mcs, name, bases, attr)
        funny = getattr(test_cls, 'perform')
        # 根据传入的测试数据 参数attr ，来遍历这个属性Cases - attr['Cases']
        for index, case in enumerate(attr['Cases']):
            # 动态给test_cls这个类添加属性 - 测试方法
            # 方法使用继承自BaseApiCase中的perform
            method = test_value(funny, case)
            setattr(test_cls, 'test_{}'.format(index), method)
        # else: # 不能删除,继承自父类的方法属性, 修改方法名,让unittest不认为是测试方法
        #     delattr(test_cls, 'test_perform')
        # 返回测试类
        return test_cls

    pass


# 通过自定义的元类创建了一个类
# Henry = MyMateClass('Henry', (object, ), {})
# 传入的用例数据Cases， 然后根据用例数据动态生成测试方法
# Henry = MyMateClass('Henry', (unittest.TestCase, ), {'Cases': [1, 23, 13]})
#
# print()


class BaseApiCase:
    """用例执行的基类"""

    def perform(self, case):
        """用例执行方法, 接收用例数据case"""
        print('test cases:', case)
        # 1. 用例数据的处理
        # 2. 接口请求
        # 3. 响应数据提取
        # 4. 断言
        pass


# 继承unittest.TestCase， 再继承BaseApiCase 用来使用其用例测试方法
My = MyMateClass('Henry', (unittest.TestCase, BaseApiCase),
                 {'Cases': [1, 2, 33]})
print(My)
# suite = unittest.defaultTestLoader.loadTestsFromTestCase(My)
# unittest.main()

with open('case.json', 'r') as file:
    cases = json.load(file)
    # 第二种
    # result = file.read()
    # cases = json.loads(result)

print(cases)
cases_dict = dict(Cases=cases)
MyData = MyMateClass('Henry', (unittest.TestCase, BaseApiCase), cases_dict)

# yaml配置文件读取
with open('api_data.yml', 'r') as f2:
    cases2 = yaml.load(f2, Loader=yaml.SafeLoader)

print(cases2)
