#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/2 20:22
# @Author : Henry
import socket

# socket
# 简称套接字， 是进程间(如两套独立系统)通信的一种方式， 它与其他进程间通信的一个主要不同是：
# 它能实现不同主机间的进程通信（通过网络），我们网络上各式各样的服务大都是基于socket来完成通信的，如浏览网页，QQ聊天，收发email等

# 创建socket
# socket.socket(Family, Type)
# Family: 可以选择socket.AF_INET(用于internet进程间通信)或者socket.AF_UNIX(用于同一台机器进程间通信)，实际工作常用AF_INET
# Type: 套接字类型， 可以是socket.SOCK_STREAM(流式套接字，主要用于TCP协议) 或者 socket.SOCK_DGRAM(数据报套接字，主要用于UDP协议)


#  实现TCP -- 传输层
"""==== 服务端 ===="""
# # 第一步： 创建一个TCP的套接字
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # 第二步： 绑定ip和端口： 方法bind
# sock.bind(('127.0.0.1', 8989))
#
# # 第三步： 开启监听
# # 传入参数100， 客户端连接服务端的最大数
# sock.listen(100)
# while True:  # 死循环， 服务端一致处在运行状态
#     # 第四步： 等待客户端发起请求， 建立连接
#     cil_sock, address = sock.accept()
#     # 第五步： 接收客户端传递的数据 （字节为单位）（默认接收到的时二进制数据）
#     content = cil_sock.recv(1024)
#     print(content.decode())
#
#     # 第六步： 给客户端返回数据 (encode()， 转成二进制数据）
#     response = 'connect successfully'.encode()
#
#     # 关闭处理客户端会话的套接字
#     cil_sock.close()

# 最后： 关闭套接字
# sock.close()


#  封装
class TCPServer:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 8989))
        self.sock.listen(100)

    def run(self):
        cil_sock, address = self.sock.accept()
        # 第五步： 接收客户端传递的数据 （字节为单位）（默认接收到的时二进制数据）
        content = cil_sock.recv(1024)
        print(content.decode())

        # 第六步： 给客户端返回数据 (encode()， 转成二进制数据）
        response = 'connect successfully'.encode()

        # 关闭处理客户端会话的套接字
        cil_sock.close()





