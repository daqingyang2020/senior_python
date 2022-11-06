#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/10/26 
# @Author  : henry
# @File    : exercise_9.py
import time
from threading import Thread


# 一、面试简单题
# 1、python的线程有什么缺陷？
# 答： python中存在全局解释器锁（GIL）， 所以同一时间只能执行一个python线程， 多线程之间是属于并发状态
#  无法利用多核cpu执行并行任务

# 二（编程题）、一个列表中有100个url地址,每个地址请求一次，请设计程序一个程序，
# 使用4个线程去发送这 100个请求（假设请求每个地址需要0.5秒，请求的代码用time.sleep(0.5)代替）,
# 计算一共需要多长时间计算出总耗时！


urls = ['www.{}.com'.format(i) for i in range(100)]
# print(urls)


def send_request(address):
    """模拟地址请求"""
    for i in range(len(address)):
        print(address[i])
        time.sleep(0.5)


def request():
    while urls:
        url = urls.pop()
        print(url)
        time.sleep(0.5)

def main():
    start_time = time.time()
    # s1 = Thread(target=send_request, args=(urls[:25], ))
    # s2 = Thread(target=send_request, args=(urls[25:50], ))
    # s3 = Thread(target=send_request, args=(urls[50:75], ))
    # s4 = Thread(target=send_request, args=(urls[75:], ))
    # 多个线程执行同一个任务函数
    s1 = Thread(target=request)
    s2 = Thread(target=request)
    s3 = Thread(target=request)
    s4 = Thread(target=request)
    s1.start()
    s2.start()
    s3.start()
    s4.start()
    s1.join()
    s2.join()
    s3.join()
    s4.join()
    end_time = time.time()
    print('Time has passed:', end_time - start_time)


if __name__ == '__main__':
    start = time.time()
    ts = []
    for i in range(4):
        t = Thread(target=request)
        t.start()
        ts.append(t)

    for t in ts:
        t.join()
    end = time.time()
    print('Time: ', end - start)
