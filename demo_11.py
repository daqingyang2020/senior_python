#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/28 20:11
# @Author : Henry
from time import time
from time import sleep
from os import getpid, getppid
from queue import Queue
from queue import LifoQueue
from queue import PriorityQueue
from multiprocessing import Process
# 进程模块中也有Queue类，设置下别名区分
from multiprocessing import Queue as ProcessQueue

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
num = 0


def add1():
    global num
    for t in range(10000):
        num += 1
    print('pid', getpid(), 'add1: ', num)
    print('parent pid', getppid(), 'add1: ', num)


def add2():
    global num
    for s in range(20000):
        num += 1
    print('pid', getpid(), 'add2: ', num)
    print('parent pid', getppid(), 'add2: ', num)


# 创建进程
# p = Process(target=add1)
# p.start()
# p2 = Process(target=add2)
# p2.start()
#
# p.join()
# p2.join()
# print('主进程process:', num)
#  未放在if __name__ == '__main__':语句下，程序报错， 进程之间资源独立
# 进程运行时所需要的代码和数据会单独拷贝一份， python文件运行时从上往下，加载一遍（类似模块导入）
# 遇到process语句， 会单独拷贝一份，再次进行加载，导致循环加载。
# 放入if __name__ == '__main__':语句下解决（加载py模块时，此条件下的语句不会执行）
# RuntimeError:
#         An attempt has been made to start a new process before the
#         current process has finished its bootstrapping phase.
#         This probably means that you are not using fork to start your
#         child processes and you have forgotten to use the proper idiom
#         in the main module:
#         if __name__ == '__main__':
#                 freeze_support()
#                 ...
#
#         The "freeze_support()" line can be omitted if the program
#         is not going to be frozen to produce an executable.


# 进程1：
#     代码
#     数据
#         - 线程1, 线程2 ...
# 进程2：
#     代码
#     数据
#        - 线程1, 线程2 ...
# 进程创建， 进程启动
# 注意点： Windows下程序中如果有使用多个进程， 程序入口要放到if __name__ == '__main__':下
# 和windows底层进程的实现有关

# Process可以给进程指定名字 name， 传参args 类似线程 ，
# daemon 参数 设置 是否作为守护进程 、 守护线程
# if __name__ == '__main__':
# p = Process(target=add1)
# p.start()
# # daemon设置 守护进程， 如果是守护进程daemon=True，该子进程会同主进程一起被关闭
# # p2 = Process(target=add2, daemon=True)
# p2 = Process(target=add2)
# p2.start()
# # 获取进程id
# # pid = getpid()
# # print('pid:', pid)
# # p.join()
# # p2.join()
# print('pid', getpid(), '主进程process:', num)

""" ============= 进程间的通信 ， 使用进程模块中封装的Queue ====="""
# 进程之间的数据共享（进程通信）
# 1. 在主进程中通过multiprocessing.Queue创建一个队列
# 2. 在创建子进程的时候，将队列当成参数传入各个子进程
# 3.在子进程中使用队列中的数据
# queue.Queue 和 multiprocessing.Queue有什么区别?
# queue.Queue: 只能在同一个进程的多个线程之间使用
# multiprocessing.Queue: 可以在多个进程之间跨进程传输数据
#
# urls = ProcessQueue()
# for i in range(100):
#     urls.put('www.{}.com'.format(i))
#
#
# # def send():
# #     while not urls.empty():
# #         url = urls.get()
# #         print(url)
# #         sleep(0.5)
#
# def send(queue_data):
#     while not queue_data.empty():
#         url = queue_data.get()
#         print(url)
#         sleep(0.5)
#
#
# def main(your_data):
#     # def main():
#     start = time()
#     ts = []
#     for v in range(4):
#         # 队列用参数到进程中
#         p = Process(target=send, args=(your_data,))
#         # p = Process(target=send)
#         p.start()
#         ts.append(p)
#
#     for u in ts:
#         u.join()
#     end = time()
#     print('time is:', end - start)
#
#
# if __name__ == '__main__':
#     main(urls)

"""=======线程池 和 进程池 ============="""
# 当需要创建的子进程不多时,可以之间利用multiprocess中的Process动态生成多个进程,
# 但如果时成百上千的目标,手动创建进程的工作量巨大,此时可以利用multiprocessing模块提供的Pool方法

# 初始化Pool时,可以指定一个最大进程数,当有新的请求提交到Pool中时,
# 如果池还没有满, 那么就会创建一个新的进程来执行该请求; 但如果池中的进程数已经达到指定的最大值,
# 那么请求就会等待, 直到池中的进程被释放, 才会用之前的进程来执行新的任务

"""=======homework============="""
# 按照下列需求实现一个生产者消费者模式:
# 1、用一个队列来存储数据
# 2、创建一个专门生产数据的任务函数，循环生产数据，当队列中数据数量少于50时，开始生产数据，
# 每次生产200个数据，添加到队列中，每生产完一轮 暂停1秒

# 3、创建一个专门获取数据的 任务函数  ，循环获取数据，
# 当队列中数据数量  大于10时就开始获取，,循环获取，每次获取20个。当 队列中数据数量  少于10的时候，暂停2秒

# 4、 创建一个进程执行生产数据的任务函数 ，5个进程执行获取数据的任务函数
