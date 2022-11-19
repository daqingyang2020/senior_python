#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/11/18 
# @Author  : henry
# @File    : exercise_12.py
import re
import socket
import json
from concurrent.futures import ThreadPoolExecutor

"""
Socket编程练习：
1、基本要求：使用Socket实现一个可以根据不同访问路径，返回不同结果的简易版HTTP服务器

2、扩展要求1：实现同一个路径，不同的请求方法，返回不同的数据
    思路提示：判断请求的方法，返回不同的数据

3、扩展要求2：再上面的两个要求的基础实现一个登录接口(不计分，做不出来没关系)：
    接口路径：/user/login
    请求方法:post
    参数：
        user:用户名
        pwd:登录密码
    请求参数类型：Content-Type:application/json
    返回数据示例：
        账号密码正确返回：{'code':1,'msg':'登录成功'}
        账号密码错误返回：{'code':0,'msg':'账号密码有误'}
        其他异常情况(参数为空,参数格式错误等等)，返回按上述数据格式，内容不做限制

    思路提示：
        1、从请求数据中提取：请求方法，请求路径，请求头，请求参数
        2、先判断请求路径，如果是/user/login
        3、在判断请求方法
        4、在判断请求参数
        5、校验参数中的账号密码
"""


def deal_param(param_str):
    p_list = param_str.split('&')
    params = {item.split('=')[0]: item.split('=')[1] for item in p_list}
    return params


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

        if req_data['path'] == '/':
            # 组装http响应报文
            data = 'HTTP/1.1 200 OK\r\n'
            data += 'Content-Type: text/html;charset=utf-8\r\n'
            data += '\r\n\r\n'
            body = '访问根路径'
            cli_sock.send((data + body).encode())
        elif req_data['path'] == '/user/login':
            if req_data['method'] == 'GET':
                data = 'HTTP/1.1 200 OK\r\n'
                data += 'Content-Type: text/html;charset=utf-8\r\n'
                data += '\r\n\r\n'
                cli_sock.send((data + 'get方法login页面').encode())
            elif req_data['method'] == 'POST':
                data = 'HTTP/1.1 200 OK\r\n'
                data += 'Content-Type: application/json;charset=utf-8\r\n'
                data += '\r\n\r\n'
                if not req_data.get('form_data'):
                    json_body = {'code': 0, 'msg': '参数为空'}
                elif req_data['form_data'].get('user') == 'Henry' and req_data['form_data'].get('pwd') == '123456':
                    json_body = {'code': 1, 'msg': '登录成功'}
                else:
                    json_body = {'code': 0, 'msg': '账号密码有误'}
                cli_sock.send(data.encode() + json.dumps(json_body).encode())
            else:
                pass
        else:
            pass
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
