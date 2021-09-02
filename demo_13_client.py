#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/9/2 20:37
# @Author : Henry
""" =====客户端====="""
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('127.0.0.1', 8989))

data = 'It is client'.encode()
sock.send(data)

content = sock.recv(1024)
print(content.decode())
