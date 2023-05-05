#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/2 20:22
# @Author : Henry
import re
import socket
import json
from concurrent.futures import ThreadPoolExecutor

# socket
# 简称套接字， 是进程间(如两套独立系统)通信的一种方式， 它与其他进程间通信的一个主要不同是：
# 它能实现不同主机间的进程通信（通过网络），我们网络上各式各样的服务大都是基于socket来完成通信的，如浏览网页，QQ聊天，收发email等

# 创建socket
# socket.socket(Family, Type)
# Family: 可以选择socket.AF_INET(用于internet进程间通信)或者socket.AF_UNIX(用于同一台机器进程间通信)，实际工作常用AF_INET
# Type: 套接字类型， 可以是socket.SOCK_STREAM(流式套接字，主要用于TCP协议)
# 或者 socket.SOCK_DGRAM(数据报套接字，主要用于UDP协议)


#  实现TCP -- 传输层
"""====TCP 服务端 ===="""
# # 第一步： 创建一个TCP的套接字
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # 第二步： 绑定ip和端口： bind方法, 传入参数元组形式， 不要使用知名端口（0-1023）
# sock.bind(('127.0.0.1', 8989)) #  通过地址和端口建立tcp连接
# print('tcp server is running at 127.0.0.1:8989')
# # 第三步： 开启监听
# # 传入参数100， 客户端连接服务端的最大数
# sock.listen(100)
#
# while True:  # 死循环， 让服务端一直处在运行状态
#     # 第四步： 等待客户端发起请求， 建立连接
#     # cil_sock：  用于客户端会话的套接字， address： 客户端地址
#     cil_sock, address = sock.accept()  # 如果没有客户端与其通信，则会阻塞
#     print('Client is connected')
#     print('Address is', address)
#     # 第五步： recv 接收客户端传递的数据 （字节为单位）（默认接收到的是二进制数据）
#     content = cil_sock.recv(1024)  # 一次接收的字节数1024
#     print('The data sent by client is:')
#     print(content.decode())  # 客户端发送过来的数据, 默认bytes（二进制形式), decode()解码转为普通字符串（python默认使用utf-8解码）
#
#     # 第六步： 给客户端返回数据 (encode(), 转成二进制数据）
#     response = 'connect successfully'
#     cil_sock.send(response.encode())
#
#     # 关闭处理客户端会话的套接字
#     cil_sock.close()
#
# # 最后： 关闭套接字
# sock.close()


#  定义类进行封装
class TCPServer:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 8989))
        self.sock.listen(100)

    def handle_request(self, cil_sock, address):
        """处理客户端请求的方法"""
        print('The client address is', address)
        content = cil_sock.recv(1024)
        print(content.decode())
        response = 'connect successfully'
        self.sock.send(response.encode())
        cil_sock.close()

    def run(self):
        # 创建线程池,设置20个线程来处理请求
        with ThreadPoolExecutor(max_workers=20) as pool:
            while True:
                cil_sock, address = self.sock.accept()
                # 当客户端建立连接后, 往线程池提交任务函数
                pool.submit(self.handle_request, cil_sock, address)


# if __name__ == '__main__':
#     tcp = TCPServer()
#     tcp.run()

# 基于TCP来实现HTTP服务端 与 客户端
# http请求报文
# http请求报文结构:

    # 请求行: 请求方法 空格 URL 空格 协议版本 回车符 换行符  （说明：此处URL不包含协议和域名）
    # 请求头:头部字段名 冒号 值 回车符 换行符
    #         ......n个请求头参数
    # 空白行: 回车符 换行符
    # 请求体: 请求体......  （如：表单数据 xx=yy&aa=bb 使用&来连接各个字段）
pass

# chrome 发送的http请求报文
"""
GET / HTTP/1.1
Host: 127.0.0.1:8989
Connection: keep-alive
Cache-Control: max-age=0
sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
sec-ch-ua-mobile: ?0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: navigate
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7
"""

# python requests 库发送的http 请求报文
"""
GET / HTTP/1.1
Host: 127.0.0.1:8989
User-Agent: python-requests/2.24.0   # User-Agent会告诉网站服务器，访问者是通过什么工具来请求的
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
"""

"""
POST / HTTP/1.1
Host: 127.0.0.1:8989
User-Agent: python-requests/2.24.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 0
"""

# url带参数 - 查询字符串参数
# requests.get('http://127.0.0.1:8989/url/login?user=henry&pwd=123456')
"""
GET /url/login?user=henry&pwd=123456 HTTP/1.1
Host: 127.0.0.1:8989
User-Agent: python-requests/2.24.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
"""

# post 请求, 使用data参数传入表单数据(字典)
# requests.post('http://127.0.0.1:8989/url/login',
#               data={'name': 'Henry', 'pwd': '654321'})
# Content-Type: application/x-www-form-urlencoded  请求头中表单格式content type
"""
POST /url/login HTTP/1.1
Host: 127.0.0.1:8989
User-Agent: python-requests/2.24.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 21
Content-Type: application/x-www-form-urlencoded # 表单格式content type

name=Henry&pwd=654321      # 请求体
"""

# post请求， 传入json关键字参数
# requests.post('http://127.0.0.1:8989/url/login', json={'name': 'Henry', 'pwd': '654321'})
# Content-Type: application/json
"""
POST /url/login HTTP/1.1
Host: 127.0.0.1:8989
User-Agent: python-requests/2.24.0
Accept-Encoding: gzip, deflate
Accept: */*
Connection: keep-alive
Content-Length: 34
Content-Type: application/json

{"name": "Henry", "pwd": "654321"}    # 请求体 json字符串
"""

"""=========基于TCP实现HTTP服务器==========="""


class HTTPServer:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 8989))
        print('Bind ip is 127.0.0.1 8989')
        self.sock.listen(100)

    def handle_request(self, cil_sock, address):
        """处理客户端请求的方法"""
        print('The client address is', address)
        # 如果客户端发过来的数据很多，处理
        content = b''
        while True:  # 循环接收
            res = cil_sock.recv(1024)
            content += res
            #  判断接收到的数据是否少于指定长度，小于则表示数据接收完毕
            if len(res) < 1024:
                break
        request_content = content.decode()
        # 调用解析数据的方法，对请求的http数据包进行解析
        body = self.parse_request(request_content)
        # print(content.decode())
        line = 'HTTP/1.1 200 OK\r\n'
        header = 'Content-Type: text/html\r\n'
        blank = '\r\n'
        response = line + header + blank
        cil_sock.send(response.encode() + body)
        cil_sock.close()

    # 对客户端发来的请求的数据内容进行解析，作进一步处理
    def parse_request(self, content):
        # 把提取的信息放入一个字典
        info = {

        }
        # 正则匹配
        lines = content.split('\r\n')
        first = lines[0]
        # 1. 获取请求方法
        method = re.search(r'(.*?) ', first).group(1)
        # 2. 获取请求的路径
        url = re.search(r' (.*?) ', first).group(1)
        # 3. 获取请求头
        # 第一次从空白行处分割， 取首个元素继续分割从第二开始切片
        header = content.split('\r\n\r\n')[0].split('\r\n')[1:]
        header_dict = {each.split(':')[0]: each.split(':')[1].strip() for each in header}
        # 4. 获取请求参数
        body_temp = content.split('\r\n\r\n')[1]
        # 判断是否有json参数， 看content-type
        if header_dict.get('Content-Type') == 'application/json':
            request_body = json.loads(body_temp)
        # 判断是否有表单参数， 看content-type
        elif header_dict.get('Content-Type') == 'application/x-www-form-urlencoded':
            body = {}
            body_list = body_temp.split('&')
            for each in body_list:
                item = each.split('=')
                body.setdefault(*item)
            else:
                request_body = body
        else:
            request_body = body_temp

        # 判断是否有查询字符串参数
        if '?' in url:
            interface_url, params = url.split('?')
            pass
        # 根据url 进行判断，返回不同的响应结果
        # 新思路 使用字典存储{'/': index, '/login': login} 路由思想
        if '/user/login' in url:
            if method == 'GET':
                response_body = 'You should use POST to login'
            else:
                response_body = self.check_login(method, '/user/login', request_body)
        elif '/test/result' in url:
            # 返回静态网页
            # 读取网页内容， 拼接响应头和响应体
            with open('reports/report.html', 'r', encoding='utf-8') as file:
                response_body = file.read()
        else:
            response_body = 'Nothing'
        return response_body.encode()

    def check_login(self, method, url, data):
        """判断登录方法"""
        if method == 'POST':
            if url == '/user/login':
                if data.get('name') == 'henry' and data.get('pwd') == 'henry123':
                    result = {'code': 1, 'msg': '登录成功'}
                else:
                    result = {'code': 0, 'msg': '账号密码有误'}
                response = json.dumps(result)
            else:
                response = 'URL not correct'
        else:
            response = 'Error method, please check!'
        return response

    def run(self):
        # 创建线程池,设置20个线程来处理请求
        with ThreadPoolExecutor(max_workers=20) as pool:
            while True:
                cil_sock, address = self.sock.accept()
                # 当客户端建立连接后, 往线程池提交任务函数
                # pool.submit(self.handle_request, cil_sock, address)
                self.handle_request(cil_sock, address)


if __name__ == '__main__':
    http = HTTPServer()
    http.run()
