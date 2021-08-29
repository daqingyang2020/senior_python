#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/26 21:20
# @Author : Henry
import time
from threading import Thread
from threading import Lock

"""并发编程"""
# 1. 多任务概念，操作系统同时运行多个任务
# cpu与多任务的关系 - 单核cpu可以执行多任务 --- 并发运行状态
# 通过操作系统调度算法，让各个任务交替执行，cpu的运算速度快，让人感觉多个任务同时进行
# 并发： 指的时任务数多余cpu核数， 系统通过调度算法让cpu ”同时“ 执行多任务
# 并行： 指的是任务数小于cpu核数，多个任务真正同时进行
"""同步 和 异步"""
# 同步 协同步调： 是指线程在访问某一资源时，获得了资源的返回结果之后才会执行其他操作（先做一件事，再做另一件事）
# 异步 步调各异：与同步相对，是指现场在访问某一资源的同时，无论是否取得返回结果，都会进行下一步操作；当有了资源返回结果时，系统自会通知线程


def work1():
    for i in range(6):
        print('work1 -- {}'.format(i))
        time.sleep(1)
    pass


def work2():
    for i in range(4):
        print('work2 -- {}'.format(i))
        time.sleep(1)
    pass


#  同步执行 执行完work1 ， 再执行work2
# work1()
# work2()

# 多线程实现多任务处理 官方库threading

# s_t = time.time()
# # 调用线程分配任务， Thread创建一个线程, target参数传入任务函数
# t1 = Thread(target=work1)
# # 启动线程 Thread.start
# t1.start()
# # 主线程的运行,从上往下, 默认情况下不会等待子线程的执行
# work2()
#
# # 主线程等待子线程的执行 Thread.join方法, 用来设置主线程等待子线程的实际
# # 默认无timeout,默认等待线程结束
# # t1.join()
# # 指定等待子线程时间
# t1.join(1)
# e_t = time.time()
# print(e_t-s_t)


#  多个线程执行同一个类似任务
# 1. 可以重写线程类的run方法,在run方法中写线程执行的具体代码
# 2. Thread 的其他初始化参数
# target -- 指定任务函数
# name -- 指定线程名
# group -- 被废弃
#  自定义线程类 -- 继承 Thread
class MyThread(Thread):
    # 重写init, 自定义参数进行传递,重写init,调用super的init, 保存参数, run方法可以获取到此参数
    def __init__(self, url):
        super(MyThread, self).__init__()
        self.url = url

    def run(self) -> None:
        arg = self.url
        print(arg)
        for i in range(10):
            time.sleep(0.1)
            # self.name 获取线程名
            print('{} request api for {} times'.format(self.name, i))
    pass


# print(Thread.__dict__)
# t2 = MyThread()
# # start 启动时执行的是run方法
# t2.start()
# 创建了10个线程,一起执行


# for t in range(10):
#     s = MyThread(name='Thread:{}'.format(t))
#     # 以线程的模式去执行run, 不能直接调用run
#     s.start()


# 任务函数带参数
def work3(worker):
    for i in range(4):
        print('{} is doing work -- {}'.format(worker, i))
        time.sleep(.5)

# 方式一
# args传递任务函数的参数, 以元组形式
# ss = Thread(target=work3, args=('Henry', ))
# ss.start()


# 方式二 kwargs 字典形式传
# ss = Thread(target=work3, kwargs={'worker': 'Henry'})
# ss.start()
#
# tt = MyThread(url='www.google.com')
# tt.start()


# 多线程之间资源是共享的。共享全局资源， 产生资源竞争问题
# 多线程共享全局变量, 可能引发资源竞争
# 多线程无法利用多核cpu的资源， 在同一时间， 只能有一个线程真正执行。
# 原因是python解释器有一个锁GIL（全局解释器锁 Global Interpreter Lock）并发状态。线程是并发执行，不能并行。
# python线程执行的切换机制：
#     1. 线程执行遇到IO耗时操作 -- time.sleep, requests.get, IO
#     2. 线程执行时间达到一个阈值 （时间非常短）
a = 0
# 创建一把锁, 仅一把锁时不会出现死锁
mutex = Lock()


def boost1():
    global a
    for i in range(1000000):
        mutex.acquire()
        # 对全局变量的修改
        a += 1  # a = a+1 -> a = __add__(a, 1) 程序可能在执行此语句时，线程进行了切换，
        # 拿着全局变量a执行另一个线程，然后返回，返回之后，此线程可能使用之前保存的值继续计算，将另一个线程执行的结果进行了覆盖
        mutex.release()
    print('boost 1 -- a', a)


def boost2():
    global a
    for i in range(1000000):
        mutex.acquire()
        a += 1
        mutex.release()
    print('boost 2 -- a', a)


#  加锁 - 互斥锁 Lock类
# 线程同步能够保证多个线程安全访问竞争资源， 最简单的同步机制是引入互斥锁
# 互斥锁为资源引入状态： 锁定和非锁定
# 某个线程要更改共享数据时，先将其锁定，此时资源的状态为锁定，
#   其他线程不能更改直到该线程释放资源，将资源的状态变成非锁定，其他线程才能再次锁定该资源
# 互斥锁保证了每次只有一个线程进行读写操作，从而保证了多线程情况下数据的正确性
# threading模块定义了Lock类，方便处理锁定：
# 创建锁
# mutex = Lock()
# # 锁定
# mutex.acquire()
# # 释放
# mutex.release()

# 注意：
#     如果这个锁之前没有上锁，那么acquire不会阻塞
#     如果在调用acquire对这个锁上锁之前已经被其他线程上了锁，那么acquire会阻塞，直到这个锁被释放

# 死锁， 逻辑上避免死锁
# 多把锁， 让多个线程进行锁定，线程之间又在等待对方释放锁，从而进入死锁


if __name__ == '__main__':

    b1 = Thread(target=boost1)
    b1.start()
    b2 = Thread(target=boost2)
    b2.start()
    b1.join()
    b2.join()
    print('main thread -- a :', a)
