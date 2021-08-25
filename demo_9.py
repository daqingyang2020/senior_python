#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/24 21:35
# @Author : Henry
import copy

""" 内存管理机制"""

""" 深浅拷贝 """
# 数据嵌套情况下，需要考虑的问题

# 浅拷贝， 拷贝数值的引用
# 列表嵌套列表：
li1 = [11, 22, 33]
li2 = li1.copy()

print(id(li1))
print(id(li2))

li1.append(13)
print(li1)
print(li2)

# 数据进行了嵌套
a = [1, 2, 3]
li = [11, 22, a]
ti = li.copy()
a.append(12)
print(li)
print(ti)


# 深拷贝，  数据的重新创建
si = copy.deepcopy(li)

a.pop()
print(li)
print(si)


ll = []
di = dict(name='Henry', age=18)
ll.append(di)

print(id(di))
print(id(ll[0]))
