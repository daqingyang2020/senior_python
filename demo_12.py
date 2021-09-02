#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/31 20:27
# @Author : Henry
import unittest
from unittestreport import TestRunner
from concurrent.futures.thread import ThreadPoolExecutor
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
# greenlet pip安装 greenlet
# gevent pip安装


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
