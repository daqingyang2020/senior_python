#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/8/17 
# @Author  : henry
# @File    : demo_5_ddt.py
import unittest
from unittestreport import TestRunner
from ddt import ddt
from ddt import data
from functools import wraps

# # 函数对象同样可以设置属性
# # 将定义的函数名看作对象，可以对其设置属性，即对象属性， 不同于函数内部定义的变量
# 当然对于python已经定义的int, str, list等对象，不可对其设置属性
# def away():
#     go = 2
#     return go

# setattr(away, 'abc', 'new')
# print(getattr(away, 'abc')) # 'new'


# ddt源码实现
def my_data(*args):  # 传入参数不固定

    def war(funny):
        # 将传入的用例数据参数保存到用例方法的属性中  setattr(funny, 'parts', args)
        funny.parts = args
        return funny
        pass

    return war


def update_test(func, value):
    @wraps(func)
    def inn(self, *args, **kwargs):
        result = func(self, value, *args, **kwargs)  # 调用方法
        return result
    return inn  # 返回inn函数， unittest认为此是测试用例, 使用wraps装饰


def my_ddt(cls):  # 接收一个类
    # 1. 获取测试类中的所有属性和方法
    # __dict__ 方法获取
    cls_dict = cls.__dict__
    for name, it in list(cls_dict.items()):  # name是属性或方法名，value是值 是测试方法的入口,
        # 给cls 加了属性， 则遍历cls.__dict__时出现runtimError， 字典长度改变了。转换成list
        # 判断遍历出来的属性或者方法是否有parts属性（则使用@my_data传递了用例数据）
        if hasattr(it, 'parts'):
            for index, value in enumerate(it.parts):  # 遍历数据时同时生成索引，以便后面加测试方法编号
                # 每遍历出一个用例数据， 将动态给用例类添加一个方法， 生成测试用例
                # 创建一个方法名
                new_name = name + str(index)

                new_function = update_test(it, value)

                # 往测试用例类中动态添加方法
                setattr(cls, new_name, new_function)  # 给cls 加属性
            else:
                # 循环结束后， 将最初的方法名删除
                delattr(cls, name)
    return cls


@my_ddt  # TestNew = my_ddt(TestNew)
class TestNew(unittest.TestCase):

    @my_data(11, 22, 33)
    def test_func(self, case):
        print(case)
        pass

    @my_data(121, 212, 353)
    def test_login(self, case):
        print(case)
        pass

    def test_other(self):
        pass


if __name__ == '__main__':

    suite = unittest.defaultTestLoader.discover('./demo_5_ddt.py')
    TestRunner(suite, templates=2).run()
    # unittest.main('demo_5_ddt.py')

# ddt 中生成用例的两个核心装饰器
# 1. data: 传入用例数据保存 --- 即通过测试方法对象的属性进行保存
# 2. ddt: 遍历用例数据，动态给测试类添加用例方法, 生成用例
