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
        print('--- decorator --')  # 被装饰函数调用之前所实现的功能
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

"""============homework========="""
# 装饰器的练习
# 1、现有有如下功能函数：
# def work(a,b):
#     res = a/b
#     print('a除B的结果为:',res)
# 调用函数当参数b为0的时候，work执行会报错！如：work(10,0)
# 需求：在不更改函数代码的前提现，实现调用work函数传入参数b为0时，函数不报错，输出结果：参数b不能为零


def zero(funny):

    def wrapper(a, b):
        if b == 0:
            print('parameter b can not be zero')
        else:
            result = funny(a, b)
            return result
    return wrapper


@zero
def work(a, b):
    res = a/b
    print('a除B的结果为:', res)


work(10, 5)
work(2, 0)

# 2、实现一个重运行的装饰器，可以用来装饰任何一个功能函数，只要被装饰的函数执行出现AssertionError，
# 则重新执行该函数，同一个函数最多重运行三次。


def rerun(stockpile):

    def coal(*args, **kwargs):
        t = 0
        while t < 3:
            try:
                stockpile(*args, **kwargs)
            except AssertionError:
                t += 1
                print('run again')
            else:
                break
    return coal
    pass


@rerun
def work2():
    assert 1 == 2


work2()

# 3、编写一个鉴权装饰器，调用被装饰的函数时，需要校验用户是否登录，如果没有登录则需要输入账号，
# 输入密码进行登录（默认正确的账号lemonban,密码123456）,
#
# 要求：只要有一个函数调用时登录成功，后续的函数都无需再输入用户名和密码
#
# 思路提示：
#     1、设置一个全局变量来保存是否登录的状态，
#     2、在装饰器中通过判断状态来决定是否要输入账号密码进行登录（登录成功之后修改登录状态）
login_flag = 0


def login():
    name = input('input login name: ')
    password = input('input password: ')
    if name == 'lemonban' and password == '123456':
        print('Login success')
        return True
    else:
        print('Name or password is not correct')
        return False


def authorize(surgeon):

    def account(*args, **kwargs):
        global login_flag
        if login_flag or int(login()):
            login_flag = 1
            result = surgeon(*args, **kwargs)
            return result
    return account


@authorize
def appearance():
    print('open system page')


@authorize
def operator():
    print('Try to add data')


appearance()
operator()
appearance()


# 4、(面试笔试题)请设计一个装饰器，接收一个int类型的参数number，可以用来装饰任何的函数，
# 如果函数运行的时间大于number，则打印出函数名和函数的运行时间
def runtime(number):
    def abc(function):
        def inner(*args, **kwargs):
            start = time.time()
            function(*args, **kwargs)
            end = time.time()
            duration = end - start
            if duration > number:
                print('function name is {}, spent {}'.format(function, duration))
        return inner
    return abc


@runtime(3)
def work_time(second):
    time.sleep(second)
    print('work over')
