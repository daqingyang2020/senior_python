#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/2 20:37
# @Author : Henry
import socket
""" =====TCP客户端====="""

#
# # 第一步 创建套接字
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # 第二步 建立连接 ， 传入服务器的地址， 元组形式的参数
# sock.connect(('127.0.0.1', 8989))
#
# # 第三步 准备数据并先服务器发送, 数据是bytes类型
# data = 'It is data from client'
# sock.send(data.encode())
#
# # 第四步 客户端接收服务端发来的回复数据
# content = sock.recv(1024)
# print(content.decode())


"""基于TCP实现HTTP客户端"""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('www.baidu.com', 80))

line = 'GET / HTTP/1.1\r\n'
header = 'Host: www.baidu.com:80\r\n'
header += 'User-Agent: python-requests/2.24.0\r\n'
header += 'Accept-Encoding: gzip, deflate\r\n'
header += 'Accept: */*\r\n'
header += 'Connection: keep-alive\r\n'
header += '\r\n'
data = line + header
sock.send(data.encode())
content = sock.recv(1024)
print(content.decode())


# http响应报文
# 状态行： 协议版本 空格 状态码 空格 状态码描述 回车符 换行符
# 响应头部：头部字段名称 冒号 值 回车符 换行符
#             ......n个响应头部
# 空白行： 回车符 或 换行符
# 响应包体： ....... （如：html，json字符串）

"""
HTTP/1.1 302 Found
Connection: keep-alive
Content-Length: 17931
Content-Type: text/html
Date: Sun, 05 Sep 2021 04:47:09 GMT
Etag: "54d97487-460b"
Server: bfe/1.0.8.18

<html>
<head>
<meta http-equiv="content-type" content="text/html;charset=utf-8">
<style data-for="result" id="css_result">
.......
"""