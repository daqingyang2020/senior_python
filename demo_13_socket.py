#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/2 20:22
# @Author : Henry
import socket



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





