#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/8/25 
# @Author  : henry
# @File    : test.py
import asyncio


# 定义协程函数
async def work():
    print('work')
    await asyncio.sleep(0.1)


res = work()  # 调用协程函数不会执行函数体，而是返回一个协程对象
asyncio.run(res)  # asyncio中的run来执行协程
