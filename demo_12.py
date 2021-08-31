#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/31 20:27
# @Author : Henry

# map函数


"""线程池并发执行测试用例"""
import unittest
from unittestreport import TestRunner
from BeautifulReport import BeautifulReport
from concurrent.futures.thread import ThreadPoolExecutor
suite = unittest.defaultTestLoader.discover('')
# # unittest report执行器
# TestRunner(suite).run(thread_count=2)

# unittest自带执行器
unittest.TextTestRunner().run(suite)

# 1. 拆分收集到的测试套件
suite_list = []
for item in suite:
    # 第一层， 测试模块级别套件
    print(item)
    for suite_cls in item:
        # 第二层， 测试类级别套件（可以再次进行遍历，得到测试方法级别套件）
        print(suite_cls)
        # 将所有测试类级别的套件加入suite list列表中
        suite_list.append(suite_cls)


#  定义要执行的测试方法
def execute(suit: unittest.TestSuite):
    # result = unittest.TextTestRunner().run(suit)
    # print(result)
    result = unittest.TestResult()
    res = suit.run(result)
    print(res)


# 2. 创建线程池去执行测试用例
with ThreadPoolExecutor(max_workers=2) as pool:
    pool.map(execute, suite_list)


"""=========协程======"""
#  greenlet pip安装 greenlet
# gevent pip安装
