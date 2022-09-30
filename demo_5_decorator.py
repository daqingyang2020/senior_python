#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/15 17:57
# @Author : Henry
import openpyxl
import pytest
import unittest
from ddt import ddt
from ddt import data
import time
#  装饰器修饰带参数的函数
# def work1(file, sheet):
#     rows = openpyxl.load_workbook(file)[sheet].rows
#     titles = [t.value for t in next(rows)]
#     return [dict(zip(titles, [s.value for s in item])) for item in rows]
# 通用装饰器， 既可以装饰有参数的函数，也可以装饰无参数函数
#  闭包函数定义不定长参数， *args， **kwargs, 让被装饰的函数自由传入参数


def decorator(func):

    def wrapper(*args, **kwargs):
        print('--- decorator start--')  # 被装饰函数调用之前所实现的功能
        result = func(*args, **kwargs)  # 当被装饰函数存在返回值时
        print('--- decorator end--')  # 被装饰函数调用之后所要实现的功能
        return result  # 返回被装饰函数的返回值， 函数返回None也不受影响
    return wrapper


@decorator
def work1():
    print('work1 ---- ')
    return 111


@decorator
def work2(a, b=None):
    print('work2: a--{} b--{}'.format(a, b))
    return 222


w1 = work1()
w2 = work2(12, b='abc')
print(w1)
print(w2)


#  装饰器装饰类

def fc(func):

    def wrapper(*args, **kwargs):
        print('--- decorator start--')
        result = func(*args, **kwargs)  # 创建类时相当于执行函数
        print('--- decorator end--')
        return result  # 相当于返回了类的实例化对象
    return wrapper


@fc  # 类当成参数传入装饰器 TestDemo = fc(TestDemo)
class TestDemo:

    def __init__(self, name, age):
        self.name = name
        self.age = age


t1 = TestDemo('henry', 19)  # 创建类时相当于执行函数
print(t1.name)


#  带参数的装饰器

def decorator(number):  # 第一层 接收装饰器参数
    def wrapper(func):  # 第二层 接收被装饰的函数
        def second_wrapper(*args, **kwargs):  # 第三层接收被装饰函数的参数
            print('The decorator argument is ', number)
            print('--- decorator start--')
            result = func(*args, **kwargs)
            print('--- decorator end--')
            return result
        return second_wrapper
    return wrapper


@decorator(10)  # simple = decorator(30)(simple)
def simple(a, b):
    print('a + b:', a+b)


simple(2, 4)


@pytest.mark.parametrize([1, 22, 3])
def test_01():
    pass


# unittest
@ddt
class TestLogin(unittest.TestCase):
    @data(11, 22, 3)
    def test_02(self, value):
        pass


# 多个装饰器装饰同一个函数
def fc(func):

    def wrapper(*args, **kwargs):
        print('--- decorator fc start--')
        result = func(*args, **kwargs)
        print('--- decorator fc  end--')
        return result
    return wrapper


def fd(func):

    def wrapper(*args, **kwargs):
        print('--- decorator fd start--')
        result = func(*args, **kwargs)
        print('--- decorator fd  end--')
        return result
    return wrapper


print()


@fc
@fd  # 先将函数通过fd进行装饰, 然后将装饰后的函数传给fc进行装饰，得到结果 fun = fc(fd(fun))
def fun(a, b):
    print('a + b:', a+b)


fun(1, 3)


# @pytest.mark('yes')
# @pytest.skip
# @pytest.mark.parametrize([11, 22])
# def test_f():
#     pass


# 装饰器的其他定义形式

# 闭包形式的装饰器： 一般用来给原功能函数调用之前或者之后做功能拓展
# 类实现装饰器： 和闭包形式装饰器作用类似
# 普通函数作为装饰器：一般是用来对被装饰的函数或类的属性进行修改 , setattr(), getattr() , hasattr()


def decorator(func):
    func.__doc__ = 'add doc for the function'
    return func  # 返回被装饰函数


@decorator    # 修改了__doc__
def new():
    print('new func----')
    print(new.__doc__)


new()
