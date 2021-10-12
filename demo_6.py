#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/17 20:41
# @Author : Henry
import sys
import logging
import random
from functools import wraps
from functools import lru_cache

#  内置装饰器 官方
# 1. functools.wraps: 用来消除装饰器的副作用(装饰后函数的名称，属性等不是原函数的)
# 2. functools.lru_cashe: 缓存装饰器， 一般用在递归上， 相同入参的函数结果缓存起来， 做到不重复调用
#     两个参数： maxsize参数设置缓存内存占用上限， 其值应当设为2幂， 值为None时表示无上限
#             typed 参数设置表示不同参数类型的调用是否分别缓存，如果设为True， 则fibonacci(5)，
#             fibonacci(5.0)将分别缓存


def star(come):

    @wraps(come)
    def wrapper():
        come()

    return wrapper


@star
def cook():
    """
    a cook method
    :return:
    """
    print('How to cook a meal')


cook()
print(cook.__doc__)  # 未使用wraps修饰时 --None
print(cook.__name__)  # 未使用wraps修饰时 -- wrapper

dic = dict(count=0)


@lru_cache()
def fibonacci(n):
    dic['count'] += 1
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


seq = fibonacci(1000)
print(seq, dic)
print(sys.getrecursionlimit())  # 最大递归深度
# fibonacci(1000)  # RecursionError: maximum recursion depth exceeded in comparison

"""=========面向对象 进阶============="""


# 魔术方法
class MyClass(object):

    def __init__(self):
        print('This is __init__')

    # 如果要控制类里面对象创建的过程，可以通过自定义new方法去实现
    def __new__(cls, *args, **kwargs):  # 用于创建对象，然后返回 一般不修改
        print('this is __new__')
        return super().__new__(cls)


m = MyClass()
print(m)

"""=========单例模式============="""


# 单例模式 一个类多次实例化 仅创建同一个对象， __new__ 方法应用
# 应用： 日志模块, python 中模块导入也是典型的单例模式


class Demo:
    __instance = None  # 私有属性，python中__开头的私有属性，实际被改名为： _类名__属性名

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            instance = super().__new__(cls)
            cls.__instance = instance
        return cls.__instance


d1 = Demo()
# Demo.instance = None  # 修改属性
# Demo.__instance = None  # 私有属性”不可修改“
d2 = Demo()
print(id(d2), id(d1))

# 日志模块单例模式的实现
#
# log = logging.getLogger('new')
# log2 = logging.getLogger('new2')
#
# log.warning('my warning')
# log2.warning('my warning 2')

#  上下文管理器 with关键字
#  上下文协议 ， 两种模式方法， __enter__, __exit__
# with 是用来启动对象的上下文管理器

with open('demo_5_decorator.py', 'r') as fi:
    print(fi)
    pass


class OpenFile:
    """
    手动实现文件操作的上下问
    """

    def __init__(self, file, method):
        # 初始化打开文件
        self.file = open(file, method)

    def __enter__(self):
        # 启动上下文时， 将打开的对象返回出去
        return self.file
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 退出上下文时， 将文件关闭
        # exc_type, exc_val, exc_tb  --- with 语句中代码执行出错， 则会将异常信息传递给此三个参数
        # 异常类型，异常值， 异常溯源
        self.file.close()
        pass


new_file = OpenFile('python.py', 'w')
with new_file as ff:
    ff.write('print("hello world")')


#  __call__ 方法， 对象的可调用， 用来实现类的对象 可调用的行为

class Definitely:
    def __call__(self, *args, **kwargs):
        print('call definitely')

    pass


def func():
    print('===func==')


c = Definitely()
print(callable(func))
print(callable(c))  # 未定义__call__ 不可调用
func()
c()


#  类实现装饰器
class Democracy:

    def __init__(self, fun):
        print('init to get the function', fun)
        self.fun = fun

    def __call__(self, *args, **kwargs):
        print('call Democracy-start-')
        self.fun()
        print('call Democracy-end-')

    pass


@Democracy  # function = Democracy(function)
def function():
    print('--- function ----')


function()

"""-----------------homework-----------------------------"""


# 魔术方法
# 1、通过装饰器实现单例模式，只要任意一个类使用该装饰器装饰， 那么就会变成一个单例模式的类。(面试真题)

class Single:
    __obj = None

    def __init__(self, psycho):
        self.psy = psycho
        pass

    def __call__(self, *args, **kwargs):
        if self.__obj is None:
            self.__obj = self.psy()
        return self.__obj
    pass


def singleton(psycho):

    def inn(*args, **kwargs):
        if not hasattr(psycho, 'var'):
            result = psycho(*args, **kwargs)
            setattr(psycho, 'var', result)
        return getattr(psycho, 'var')
    return inn


# @Single
@singleton
class Psycho:
    __inst = None

    def __init__(self):
        self.name = 'boy'


p1 = Psycho()
print(p1.name, type(p1))
p2 = Psycho()
print(id(p1),  id(p2))
assert id(p1) == id(p2)

# 2、请实现一个类，前五次创建对象，每次都可以返回一个新的对象，
# 第六次开始，每次创建，都随机返回前5个对象中的一个


class Five:
    contain = []

    def __new__(cls, *args, **kwargs):
        if len(cls.contain) < 5:
            obj = super(Five, cls).__new__(cls)
            cls.contain.append(obj)
        else:
            obj = random.choice(cls.contain)
        return obj


one = Five()
two = Five()
three = Five()
four = Five()
five = Five()
six = Five()
print(id(one), id(two), id(three), id(four), id(five), id(six))
assert id(six) in (id(one), id(two), id(three), id(four), id(five))


# 3、通过类实现一个通用装饰器，既可以装饰函数，又可以装饰器类，不管函数和类需不需要传参都可以装饰
class Common:

    def __init__(self, anything):
        self.immortal = anything

    def __call__(self, *args, **kwargs):
        if callable(self.immortal):
            print('You use Common decorator')
            result = self.immortal(*args, **kwargs)
            return result
        else:
            print('object is not callable')


@Common
class Youth:
    def __init__(self):
        self.name = 'Henry'
    pass


@Common
def mourn():
    print('Mourn for this function')
    pass


you = Youth()
print(you.name)
mourn()
