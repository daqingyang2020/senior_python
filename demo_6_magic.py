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

    @wraps(come)  # 把wrap(func)修饰在闭包函数上
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
print(cook.__doc__)  # 文档字符串注释 - 使用@star修饰函数且未使用wraps修饰时 -- 文档字符串注释为空
print(cook.__name__)  # 函数名 - 使用@star修饰函数未使用wraps修饰时 -- 函数名执行是闭包函数wrapper


dic = dict(count=0)


@lru_cache()
def fibonacci(n):  # 斐波拉契数列
    dic['count'] += 1
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# 超过默认的递归深度
# seq = fibonacci(1000)

seq = fibonacci(100)
print(seq, dic)
print(sys.getrecursionlimit())  # 最大递归深度

# fibonacci(1000)  # RecursionError: maximum recursion depth exceeded in comparison

"""=========面向对象 进阶============="""


# 魔术方法
# python中默认父类：object
class MyClass(object):

    def __init__(self):
        # 初始化方法， 第一个参数self， 对象创建完成后对其进行初始化（设置属性等）
        print('This is __init__')

    # 如果要控制类里面对象创建的过程，可以通过自定义__new__方法去实现 - 最常见的应用场景：单例模式
    def __new__(cls, *args, **kwargs):  # 用于创建并返回对象 一般不修改
        print('this is __new__')
        return super().__new__(cls)  # 来自于父类object 的__new__, 返回对象


m = MyClass()
print(m)

"""=========单例模式============="""


# 单例模式：类每次实例化的时候都会创建一个新的对象，单例模式就是类每次实例化时返回同一个对象，即第一次创建的对象。 __new__ 方法应用
# 应用： 日志模块, python 中模块导入也是典型的单例模式

#  举例单例模式
class Demo:
    __instance = None  # 私有属性，python中__开头的私有属性，实际被改名为： _类名__属性名

    # 通过重写__new__方法控制类创建对象的次数
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:  # 判断类属性
            # 创建完这个对象后，保存为类的一个属性（类属性有值了说明对象创建过了）
            instance = super().__new__(cls, *args, **kwargs)
            cls.__instance = instance
        return cls.__instance


d1 = Demo()
# Demo.instance = None  # 修改属性
# Demo.__instance = None  # 私有属性”不可直接修改“ ，提高安全性
d2 = Demo()
print('d2: ', id(d2), 'd1: ', id(d1))

# 日志模块单例模式的实现
#
# log = logging.getLogger('new')
# log2 = logging.getLogger('new2')
#
# log.warning('my warning')
# log2.warning('my warning 2')

#  上下文管理器 with关键字 -- 不止用于操作文件
#  上下文协议 ， 两种模式方法， __enter__, __exit__
# with 是用来启动对象的上下文管理器

# open 实现了上下文协议，执行with语句时，进入（with跟着的）对象的__enter__方法执行，将执行结果保存到as语句定义的变量
# with下的语句块执行完毕后，调用（with）对象的__exit__方法，结束。
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
        if exc_type:
            print(exc_type, exc_val, exc_tb)
        pass


new_file = OpenFile('albert.py', 'w')
with new_file as ff:  # new_file 对象实现了__enter__ 和 __exit__ 即可
    ff.write('print("hello world")')
    print(undefined_name)


# 上下文协议应用场景：数据库连接关闭，文件操作，webdriver操作， requests.session等


#  __call__ 方法， 使得对象可调用， 用来实现类的对象可调用的行为

class Definitely:
    # 类中实现__call__方法
    def __call__(self, *args, **kwargs):
        print('call definitely')
    pass


def func():
    print('===func==')


c = Definitely()
print(callable(func))  # True
print(callable(c))  # 未定义__call__ 时类创建的对象不可调用 - False
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

