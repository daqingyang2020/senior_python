#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/12 20:24
# @Author : Henry
import openpyxl
import unittest
from ddt import ddt
from ddt import data
import time

var = 100
tar = [1, 3]


# 纯函数
def fun1(a, b):
    """纯函数"""
    return a + b


def fun2(a):
    """非纯函数， 返回值受外部数据影响"""
    return var + a


def fun3(a, b):
    """非纯函数， 会修改外部环境数据"""
    tar.append(a)
    tar.append(b)
    return a + b


# 匿名函数，定义：lambda 参数: 表达式
# 一般给函数传递参数用， 也不建议通过变量接收lambda表达式
def my_sort(n):
    return n[1]


# sorted 函数，sort方法， 给key传递排序规则
a = [(6, 9), (1, 8), (3, 2)]
a.sort()  # 默认按照列表每个元素中的第一个值进行排序
print(a)
b = sorted(a, key=my_sort)  # key参数不使用匿名函数，传递一个具有排序规则的函数。
# 排序的时候将每个元素作为参数传递给此函数my_sort，此处传递函数名，排序时内部调用
c = sorted(a, key=lambda x: x[1])  # 使用匿名函数， 排序时将列表中的每个元素当作参数传递给lambda函数
a.sort(key=lambda x: x[1])
print(a, b, c)

# filter 函数： 过滤器
#  参数1 过滤规则函数 --- 通常用匿名函数去写这个规则
#  参数2 可迭代对象

li = [11, 33, 44, 5, 6]
# 过滤大于30 的数据， 结合匿名函数
res = filter(lambda x: x > 30, li)
# res -- filter对象，迭代器
print(res, list(res))
#  也可以用过推导式也能完成


# map函数: 将函数应用于iterable中每一项并输出其结果
# 参数1 处理函数 --- 一般匿名函数处理
# 参数2 可迭代对象

st = [22, 11, 32]
# 返回列表中数据的2次方
res2 = map(lambda x: x ** 2, st)
print(res2, list(res2))
# 推导式也可以实现


res3 = map(str, range(10))
print(''.join(res3))

# exec: 执行字符串中的python代码
# eval: 识别字符串中有效表达式
code = """
a = 100
b = 20
print(a+b)
"""
exec(code)


# all: 判断迭代对象内所有元素是否都为真, 是则返回True
def work(name=None, age=None, sex=None):
    if name and age and sex:
        print('True 1')
    if all([name, age, sex]):
        print('True 2')


work('Henry', 12, 'male')


# any: 判断迭代对象内如有任一元素为真, 则返回True
def work2(name=None, age=None, sex=None):
    if name or age or sex:
        print('True 3')
    if any([name, age, sex]):
        print('True 4')


work2('Henry')

# zip函数: 聚合打包
title = ['a', 'b', 'c']
value = [1, 2, 3]

# 普通写法， 以title的元素为键，value的元素为值形成字典
# dic = {}
# for i in range(len(title)):
#     dic[title[i]] = value[i]
# print(dic)

# 使用zip
print(dict(zip(title, value)))
print(
    dict(
        [('A', 10), ('B', 20)]
    )
)

aa = [1, 2, 3]
bb = [11, 22, 33]
cc = [111, 222, 333, 444]
print(list(zip(aa, bb, cc)))

cases = [
    ['case_id', 'case_title', 'url', 'data', 'excepted'],
    [4, '用例4', 'www.baidu.com', '002', 'ok'],
    [1, '用例1', 'www.baidu.com', '001', 'ok']
]
titles = cases[0]
for i in cases[1:]:
    res = dict(zip(titles, i))
    print(res)

result = [dict(zip(cases[0], task)) for task in cases[1:]]
print(result)


# 闭包函数
# 变量作用域 ， 内部的和全局的。
def simple():
    print('simple----')


# 实现一个闭包函数，须满足如下条件：
# 1. 函数中嵌套一个函数
# 2. 外层函数返回内层函数的变量名
# 3. 内层函数对外部作用域有一个非全局的变量进行引用

# 函数中定义函数
def funcb1():
    x = 100

    def funcb2():
        c = x * 2
        print(c)

    return funcb2


res = funcb1()
print(res)
res()


# 无法直接在外部调用内部函数funcb2
# 通过return把内部函数名返回, 然后调用
# funcb2变量作用域 ， 内部的， funcb1的和全局的。
# funcb2引用了funcb1的x 变量，没有引用外部全局变量
# 闭包函数 = 函数 + 保存引用数据的封闭作用域
# 闭包函数可以引用外层作用域的传入的参数，和其定义的局部变量


# 装饰器
# def decorator(a):
#
#     def wrapper():
#         print('wrapper --- start')
#         print(a)  # a 可以是传进来的work函数
#         a()  # 调用
#         print('wrapper --- over')
#
#     return wrapper
#
#
# def work():
#     print('work-------')
#
#
# fun = decorator(work)
# print(fun)
# work = decorator(work)
# print(work)


def decorator(func):
    def wrapper():
        print('wrapper --- start')
        print(func)  # 传进来的函数
        func()  # 调用传进来的函数
        print('wrapper --- over')

    return wrapper


@decorator  # ----> work_demo = decorator(work_demo)
def work_demo():
    print('work demo --- func')


# 开放封闭原则
# 开放封闭原则： 软件实体应该是可扩展的，而不可修改的。也就是说，对扩展是开放的，而对修改是封闭的。
# 装饰器的作用： 在不更改原功能函数内部代码，并且不改变调用方法的情况下为原代码添加新的功能。


# ddt - 装饰器的应用


@ddt()
class TestDemo(unittest.TestCase):

    @data(11, 22, 33)
    def test_login(self, case):
        print(case)
        pass


# 需求：使用装饰器来统计函数运行的时间

def time_spent(func):
    def wrapper():
        # 获取功能函数执行之前的时间
        start = time.time()
        func()
        # 结束时间
        end = time.time()
        print('The function {} spent {}'.format(func, end - start))

    return wrapper


@time_spent  # work1 = time_spent(work1)
def work1():
    for t in range(3):
        time.sleep(0.5)


def work2():
    for s in range(3):
        time.sleep(0.7)


work1()
work2()
