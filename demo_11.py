#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/28 20:11
# @Author : Henry
from queue import Queue
from queue import LifoQueue
from queue import PriorityQueue
from multiprocessing import Process
# 队列
# 队列模块 内置模块
# 先入先出



# 实例化一个队列对象, 可指定队列长度maxsize
q = Queue(2)  # 若满了,会阻塞
# 队列添加数据
# 队列操作的方法: put
q.put('python01')
q.put('python02')
# q.put('python03', timeout=1)  # 参数timeout设置等待时间, raise Full

# 方法: 获取队列中数据的长度
ll = q.qsize()
print(ll)

# 获取数据 get, 当队列为空, 再get会阻塞
data = q.get()
print(data)
data = q.get()
print(data)
# data = q.get(timeout=1) # raise Empty

# 添加数据不等待， 数据已满的话直接报错
q.put_nowait('python03')

# 获取数据不等待，
q.get_nowait()  # q.get(block=False)

# 判断队列是否为空， 判断队列是否已满
q.empty()  # True or False
q.full()
print('--')
# task_done , join
# task_done 先队列发出一条任务完成的信号
# join 等待队列中的任务执行全部完毕
qq = Queue(3)
qq.put(11)
qq.put(22)
qq.put(33)
qq.get()
qq.get()
qq.get()
qq.task_done()
qq.task_done()
qq.task_done()
print('join - 1')
qq.join()
print('join - 2')


#  LifoQueue  先入后出
lq = LifoQueue()
lq.put(11)
lq.put(22)
print(lq.get())  # 继承方法的思想

# PriorityQueue 优先级队列 可以设置优先级 (优先级， 数据）
lp = PriorityQueue()
lp.put((2, '222'))
lp.put((6, '126'))
lp.put((3, '123'))
# 优先级数值越小， 优先级越高， 越先出队列
print(lp.get())


# 通过队列保证线程数据的安全性
que = Queue()
que.put(0)


def work1():
    for i in range(100000):
        a = que.get()
        a += 1
        que.put(a)


def work2():
    for i in range(100000):
        a = que.get()
        a += 1
        que.put(a)


""" ==== 进程 ==== """
# 进程间资源不共享，相互独立

# 一个程序运行起来后，代码+用到的资源称之为进程，是操作系统分配资源的基本单元
# 状态： 就绪状态， 执行状态， 等待状态

# 进程 线程对比
# 功能：
# 进程， 能够完成多任务，比如在一台电脑上能够同时运行多个软件
# 线程， 能够完成多任务， 比如 一个QQ中多个聊天窗口 ， 相关的资源共享
# 定义的不同
# 进程是系统进行资源分配单位


# 创建进程
p = Process(target=work1)
p.start()
p2 = Process(target=work2)
p2.start()

p.join()
p2.join()
print('主进程')


# 进程1：
#     代码
#     数据
#         - 线程1, 线程2 ...
# 进程2：
#     代码
#     数据
#        - 线程1, 线程2 ...
# 进程创建， 进程启动
# 注意点： Windows下程序中如果有多个进程，  程序入口要放到  if __name__ == '__main__':下
