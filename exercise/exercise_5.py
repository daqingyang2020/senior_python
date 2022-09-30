#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/9/8 
# @Author  : henry
# @File    : exercise_5.py
import time
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


def zero_try(funny):

    def wrapper(a, b):
        # 异常捕获方式
        try:
            return funny(a, b)
        except ZeroDivisionError:
            print('b can not be zero')
    return wrapper


@zero_try
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
        while t < 4:
            try:
                if t == 0:
                    print('start')
                else:
                    print(f'rerun {t} times')
                result = stockpile(*args, **kwargs)
            except AssertionError as e:
                t += 1
                if t == 4:
                    raise e
                print('fail')
            else:
                print('pass')
                return result
    return coal
    pass


@rerun
def work2():
    assert 1 == 1


work2()

# 3、编写一个鉴权装饰器，调用被装饰的函数时，需要校验用户是否登录，如果没有登录则需要输入账号，
# 输入密码进行登录（默认正确的账号lemonban,密码123456）,
#
# 要求：只要有一个函数调用时登录成功，后续的函数都无需再输入用户名和密码
#
# 思路提示：
#     1、设置一个全局变量来保存是否登录的状态，
#     2、在装饰器中通过判断状态来决定是否要输入账号密码进行登录（登录成功之后修改登录状态）
login_flag = False


def login():
    global login_flag
    name = input('input login name: ')
    password = input('input password: ')
    if name == 'lemonban' and password == '123456':
        print('Login success')
        login_flag = True
        return True
    else:
        print('Name or password is not correct')
        return False


def authorize(surgeon):

    def account(*args, **kwargs):
        global login_flag
        if login_flag or login():
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
            res = function(*args, **kwargs)
            end = time.time()
            duration = end - start
            if duration > number:
                print('function name is {}, spent {}'.format(function, duration))
            return res
        return inner
    return abc


@runtime(3)
def work_time(second):
    time.sleep(second)
    print('work over')
