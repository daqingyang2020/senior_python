#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/9/30 
# @Author  : henry
# @File    : exercise_6.py
import random


# 魔术方法
# 1、通过装饰器实现单例模式，只要任意一个类使用该装饰器装饰， 那么就会变成一个单例模式的类。(面试真题)
# 函数实现
def single(cls):
    def inner(*args):
        if not hasattr(cls, 'instance'):  # 不能直接用cls.instance判断，因为可能没有这个属性
            res = cls(*args)
            cls.instance = res  # 设置属性，cls.instance这个形式来设置属性，或者使用setattr
        return cls.instance  # 或getattr

    return inner


# 类实现
class Single:
    def __init__(self, cls):
        self.obj = cls

    def __call__(self, *args, **kwargs):
        if not hasattr(self.obj, 'instance'):
            res = self.obj(*args, **kwargs)
            self.obj.instance = res
        return self.obj.instance


# @single
@Single
class Psycho:
    def __init__(self, *args):
        print(args)

    pass


c1 = Psycho(234)
c2 = Psycho(123)
print(c1, c2)


# 2、请实现一个类，前五次创建对象，每次都可以返回一个新的对象，第六次开始，每次创建，都随机返回前5个对象中的一个


class Five:
    __contain = []

    def __new__(cls, *args, **kwargs):
        if len(cls.__contain) < 5:
            obj = super(Five, cls).__new__(cls)
            cls.__contain.append(obj)
        else:
            obj = random.choice(cls.__contain)
        return obj


one = Five()
two = Five()
three = Five()
four = Five()
five = Five()
six = Five()
print(id(one), id(two), id(three), id(four), id(five), id(six), sep='\n')
assert id(six) in (id(one), id(two), id(three), id(four), id(five))


# 3、通过类实现一个通用装饰器，既可以装饰函数，又可以装饰器类，不管函数和类需不需要传参都可以装饰
class Common:

    def __init__(self, anything):
        self.immortal = anything

    def __call__(self, *args, **kwargs):
        print('You use Common decorator')
        result = self.immortal(*args, **kwargs)
        return result


# 函数实现
def common(item):
    def wrapper(*args, **kwargs):
        print('You use common decorator')
        res = item(*args, **kwargs)
        return res

    return wrapper


@Common
class Youth:
    def __init__(self):
        self.name = 'Henry'

    pass


@common
def mourn():
    print('Mourn for this function')
    pass


you = Youth()
print(you.name)
mourn()
