#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/10/28 
# @Author  : henry
# @File    : exercise_10.py
from os import getpid
from time import sleep
from multiprocessing import Manager
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from queue import Queue

"""设计模式： 生产者消费者模式"""
# 按照下列需求实现一个生产者消费者模式:
# 1、用一个队列来存储数据
# 2、创建一个专门生产数据的任务函数，循环生产数据，当队列中数据数量少于50时，开始生产数据，
# 每次生产200个数据，添加到队列中，每生产完一轮 暂停1秒
# 3、创建一个专门获取数据的 任务函数，循环获取数据，
# 当队列中数据数量  大于10时就开始获取，循环获取，每次获取10个。当 队列中数据数量少于10的时候，暂停2秒
# 4、 创建一个进程执行生产数据的任务函数 ，5个进程执行获取数据的任务函数


def generate_data(queue):
    """生产者，生产数据任务， 将队列作为参数传入进行处理"""
    data = 0
    count = 0
    while True:
        if queue.qsize() < 50:
            for dd in range(data, data + 200):
                queue.put(dd)
                print('pid-{}--add data: {}'.format(getpid(), dd))
            print('pid-{}-generate data done-{}'.format(getpid(), count))
            count += 1
            sleep(1)


def consume_data(queue):
    """消费者， 消费数据任务， 将队列作为参数传入进行处理"""
    while True:
        if queue.qsize() >= 10:
            for j in range(10):
                res = queue.get()
                print('pid-{}--get data: {}'.format(getpid(), res))
            print('pid-{}-consume data done'.format(getpid()))
        else:
            sleep(2)


if __name__ == '__main__':
    # 使用进程池， 通讯使用Manager().Queue()
    process_queue = Manager().Queue()
    with ProcessPoolExecutor(max_workers=6) as pool:
        # 1个进程生成数据
        pool.submit(generate_data, process_queue)
        # 5个进程消费数据
        for i in range(5):
            pool.submit(consume_data, process_queue)
        pool.shutdown()

    # 使用线程池，  通讯使用queue.Queue()
    my_queue = Queue()
    with ThreadPoolExecutor(max_workers=6) as pool:
        pool.submit(generate_data, my_queue)
        for i in range(5):
            pool.submit(consume_data, my_queue)
        pool.shutdown()
