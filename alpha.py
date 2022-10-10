#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/9/30 
# @Author  : henry
# @File    : alpha.py
class Mark:

    def play(self, func):
        def wrapper(*args, **kwargs):
            print('==play==')
            return func(*args, **kwargs)

        return wrapper


mark = Mark()  # 创建好对象，让其他模块用
