#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/12 20:24
# @Author : Henry
import openpyxl
import unittest
from ddt import ddt
from ddt import data
import time
# 匿名函数， 一般给函数传参数
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
res2 = map(lambda x: x**2, st)
print(res2, list(res2))
# 推导式也可以实现


# exec: 执行字符串中的python代码
# eval: 识别字符串中有效表达式
code = """
a = 100
b = 20
print(a+b)
"""
exec(code)


# all: 判断迭代对象内所有元素是否为真, 是则返回True
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
    def test_login(self):
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


""" -------------homework---------------"""

# 1、通过上述上课所学内置函数和推导式的语法，读取附件中excel文件，转换为如下的格式：
# res1 = [ {'case_id': 1, 'case_title': '用例1', 'url': 'www.baudi.com', 'data': '001', 'excepted': 'ok'},
#  {'case_id': 4, 'case_title': '用例4', 'url': 'www.baudi.com', 'data': '002', 'excepted': 'ok'},
#  {'case_id': 2, 'case_title': '用例2', 'url': 'www.baudi.com', 'data': '002', 'excepted': 'ok'},
#  {'case_id': 3, 'case_title': '用例3', 'url': 'www.baudi.com', 'data': '002', 'excepted': 'ok'},
#  {'case_id': 5, 'case_title': '用例5', 'url': 'www.baudi.com', 'data': '002', 'excepted': 'ok'} ]
# 2、对第一题读取出来的数据，按照case_id字段进行排序。
# 3、将读取出来的数据中的method字段值 统一修改为GET（不需要修改excel，只对读出来的数据进行修改）
# 1.
book = openpyxl.load_workbook('data.xlsx')
sheet = book.active
lines = sheet.values
title = next(lines)
res1 = []
for each in lines:
    res1.append(dict(zip(title, each)))

# 2.
res1.sort(key=lambda x: x['case_id'])
print(res1)

# 3.
for it in res1:
    it['method'] = 'GET'
print(res1)

result2 = [item.update({'method': 'GET'}) or item for item in res1]