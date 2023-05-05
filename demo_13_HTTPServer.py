#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/11/9 
# @Author  : henry
# @File    : test_1.py
import re
import socket
import json
from concurrent.futures import ThreadPoolExecutor

urls = {}


def route(path):
    def wrapper(func):
        urls[path] = func
        return func
    return wrapper


def deal_param(param_str):
    p_list = param_str.split('&')
    params = {item.split('=')[0]: item.split('=')[1] for item in p_list}
    return params


@route('/')
def index(req_data):
    """访问根路径的处理"""
    data = 'HTTP/1.1 200 OK\r\n'
    data += 'Content-Type: text/html;charset=utf-8\r\n'
    data += '\r\n\r\n'
    body = '访问根路径'
    return (data + body).encode()


def login(req_data):
    """登录的处理"""
    if req_data['method'] == 'GET':
        data = 'HTTP/1.1 200 OK\r\n'
        data += 'Content-Type: text/html;charset=utf-8\r\n'
        data += '\r\n\r\n'
        data += 'get方法login页面'
        return data.encode()
    elif req_data['method'] == 'POST':
        data = 'HTTP/1.1 200 OK\r\n'
        data += 'Content-Type: application/json;charset=utf-8\r\n'
        data += '\r\n\r\n'
        if not req_data.get('form_data'):
            json_body = {'code': 0, 'msg': '参数为空'}
        elif req_data['form_data'].get('user') == 'Henry' and req_data['form_data'].get('pwd') == '123456':
            # 实际应用中用户名密码存储在数据库，且密码通过密文传输，需调用加密解密算法
            json_body = {'code': 1, 'msg': '登录成功'}
        else:
            json_body = {'code': 0, 'msg': '账号密码有误'}
        return data.encode() + json.dumps(json_body).encode()


def register(req_data):
    """模拟用户注册的处理"""
    data = 'HTTP/1.1 200 OK\r\n'
    data += 'Content-Type: text/html;charset=utf-8\r\n'
    data += '\r\n\r\n'
    data += 'register页面'
    return data.encode()


def error_404():
    """404页面"""
    data = 'HTTP/1.1 404 Not Found\r\n'
    data += 'Content-Type: text/html;charset=utf-8\r\n'
    data += '\r\n\r\n'
    data += '404页面'
    return data.encode()


class TCPServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 8999))
        self.sock.listen(100)

    # 线程执行函数
    def handle_request(self, cli_sock, address):
        """处理客户端请求的方法"""
        print('客户端地址：{}'.format(address))
        # 如果客户端发过来的数据很多，优化处理，循环接收数据
        content = b''
        while True:
            res = cli_sock.recv(1024)
            content += res
            if len(res) < 1024:
                break
        cli_data = content
        cli_data = cli_data.decode()
        print('客户端发送数据:', cli_data)
        print('客户端建立连接')
        req_data = self.parser_request(cli_data)

        handle_func = urls.get(req_data['path'])
        if handle_func:
            data = handle_func(req_data)
        else:
            data = error_404()
        # if req_data['path'] == '/':
        #     data = index()
        # elif req_data['path'] == '/user/login':
        #     data = login(req_data)
        # else:
        #     data = error_404()
        cli_sock.send(data)
        cli_sock.close()

    def parser_request(self, content: str):
        """
        解析后返回请求数据
        :param content:
        :return: info
        """
        info = {}
        lines = content.split('\r\n')
        # 请求方法
        info['method'] = re.search(r'\w+', lines[0]).group()
        # 请求路径
        path = re.search(r'(/.*?) ', lines[0]).group(1)
        temp = content.split('\r\n\r\n')
        header_list = temp[0].split('\r\n')[1:]
        # 请求头
        headers = {i.split(': ')[0]: i.split(': ')[1] for i in header_list}
        info['headers'] = headers
        # 请求体
        body = temp[1]
        # 判断查询字符串参数
        if '?' in path:
            info['path'], param = path.split('?')
            info['params'] = deal_param(param)
        else:
            info['path'] = path
        # 判断 表单参数, json参数
        if headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            info['form_data'] = deal_param(body)
        elif headers.get('Content-Type') == 'application/json':
            info['json_data'] = json.loads(body)
        else:
            pass
        return info

    def run_server(self):
        # 创建一个线程池， 设置线程
        with ThreadPoolExecutor(max_workers=20) as pool:
            while True:
                cli_sock, address = self.sock.accept()
                # 当客户端建立连接后，向线程池提交处理任务
                pool.submit(self.handle_request, cli_sock, address)


if __name__ == '__main__':
    TCPServer().run_server()
    pass
