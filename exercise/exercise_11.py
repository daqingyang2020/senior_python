#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/11/7 
# @Author  : henry
# @File    : exercise_11.py
import unittest
from concurrent.futures import ThreadPoolExecutor


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
    result_dict['errors'] += len(result.errors)
    result_dict['failures'] += len(result.failures)
    result_dict['run'] += result.testsRun
    pass


with ThreadPoolExecutor(max_workers=2) as pool:
    pool.map(running, test_list)
    pool.shutdown()
    print('Final Result:', result_dict)
    print('Thread over')
