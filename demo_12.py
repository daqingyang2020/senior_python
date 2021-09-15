#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/31 20:27
# @Author : Henry
from gevent.monkey import patch_all
# gevent.monkey调用补丁， 放置最前 ，不然MonkeyPatchWarning
# patch_all()
import asyncio
import unittest
from unittestreport import TestRunner
from concurrent.futures.thread import ThreadPoolExecutor
from greenlet import greenlet
import gevent
# from BeautifulReport import BeautifulReport

# map函数


"""线程池并发执行测试用例"""

# suite = unittest.defaultTestLoader.discover('')
# # # unittest report执行器
# # TestRunner(suite).run(thread_count=2)
#
# # unittest自带执行器
# unittest.TextTestRunner().run(suite)
#
# # 1. 拆分收集到的测试套件
# suite_list = []
# for item in suite:
#     # 第一层， 测试模块级别套件
#     print(item)
#     for suite_cls in item:
#         # 第二层， 测试类级别套件（可以再次进行遍历，得到测试方法级别套件）
#         print(suite_cls)
#         # 将所有测试类级别的套件加入suite list列表中
#         suite_list.append(suite_cls)
#
#
# #  定义要执行的测试方法
# def execute(suit: unittest.TestSuite):
#     # result = unittest.TextTestRunner().run(suit)
#     # print(result)
#     result = unittest.TestResult()
#     res = suit.run(result)
#     print(res)
#
#
# # 2. 创建线程池去执行测试用例
# with ThreadPoolExecutor(max_workers=2) as pool:
#     pool.map(execute, suite_list)


"""=========协程======"""


# greenlet pip安装
# gevent pip安装

# 原生协程  关键字 async await

# 定义协程函数
async def work():
    for i in range(10, 13):
        print(i)


# 调用协程函数，返回一个协程对象
res = work()
# 执行协程
asyncio.run(res)


# greenlet

# gevent
def test1():
    for i in range(3, 9):
        print(i)
        # 模拟i/o等耗时
        gevent.sleep(.1)
    pass


def test2():
    for i in range(21, 27):
        print(i)
        # 模拟i/o等耗时
        gevent.sleep(.2)
    pass


# 任务函数加入协程
g1 = gevent.spawn(test1)
g2 = gevent.spawn(test2)

# 任务函数等待并开始执行
g1.join()
g2.join()

print('====over====')

"""线程  进程  协程 之间的对比"""
# 1. 进程是操作系统资源分配的基本单位
# 2. 线程是操作系统的调度的基本单位
# 3. 协程存在与线程之中， 本质上是一个特定情况下可以切换的特殊的函数
# 4. 进程间由于资源相互独立，每次切换所耗资源很大，耗时更长
# 5. 线程的切换涉及到用户空间 和 内核空间的切换， 需要操作系统调度，
# 而且除了涉及和协程相同的cpu上下文之外，还有线程私有的栈和寄存器等，效率一般
# 6.协程是切换任务， 只涉及到cpu上下文， 资源消耗小，几乎可以忽略不计
# 7. 多进程、多线程根据cpu核数不一样可能是并行的， 但是协程是在一个线程中，所以是并发。
# 注意点：在python中，由于存在GIL， 多线程并不能实现并行。要充分利用cpu还是需要通过多进程来实现
# 适用场景：
# 进程：计算密集型任务（如：大规模的数据计算和处理）
# 线程： IO密集型的任务（如：文件读写、网络请求多的任务）
# 协程：IO密集型项目且要求高并发（如：用locust压测使用的是协程）实际上真实项目中对应高并发的业务并不会使用python语言

"""=============homework==============="""
# 作业要求：通过线程池或者进程池，实现一个可以并发运行unittest测试用例的方法。
# 思路提示：
#     1、每个测试套件作为一个测试任务，收集多个测试套件(任务)存储到列表或者队列中
#     2、创建线程池，设置运行最大线程数量。
#     3、依次获取任务提交到线程池中运行。
# #单个套件的运行方式提示:
# suite = 测试套件
# from unittest import TestResult
# result = TestResult()
# res = suite.run(result)

test_list = []
result_dict = dict(run=0, errors=0, failures=0)
suite = unittest.defaultTestLoader.discover('cases')

for module in suite:
    for cls_case in module:
        test_list.append(cls_case)


def running(unit_suite):
    res = unittest.TestResult()
    result = unit_suite.run(res)
    # print('running result:', result)
    result_dict['errors'] += len(result.errors)
    result_dict['failures'] += len(result.failures)
    result_dict['run'] += result.testsRun
    pass


with ThreadPoolExecutor(max_workers=2) as pool:
    pool.map(running, test_list)
    pool.shutdown()
    print('Final Result:', result_dict)
    print('Thread over')
