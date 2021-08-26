#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/24 21:35
# @Author : Henry
import copy
import sys

""" 内存管理机制"""
# python中创建对象的时候，首先会去申请内存地址，然后对对象进行初始化， 所有对象都会维护在一个叫refchain的双向循环链表中，
# 每个数据保存的信息有：（c结构体）
# 链表中数据前后数据的指针，
# 数据的类型，
# 数据值，
# 数据的引用计数，
# 数据的长度

# 引用计数机制：
# 计数增加场景：
#     对象被创建，
#     对象被别的变量引用，
#     对象作为元素放入容器中（如放入列表）
#     对象被当成参数传递到函数中
#
a = 10
b = a
print(sys.getrefcount(a))


# 引用计数的减少：
#     对象的别名被显示销毁 -- del xxx
#     对象的一个别名被赋值给其他对象
#     对象从容器中被一处，或者容器被销毁
#     一个引用离开了它的作用域（调用函数的场景）

# 当对象的引用计数为零时，对象的内存被释放


# 数据池和缓存 --- 优化内存
# python启动时会将常见的数据进行初始化，放入数据池中，不再另外开辟内存保存这类数据
# 其中整数数据 -5 - 256： python自动将-5~256的整数缓存到一个小整数池中，当你将这些整数赋值给变量时，并不会重新创建对象
# 而是使用已经创建好的缓存对象。当删除这些数据的引用变量时，数据不会被回收
#  另外还有： ASCII字符,（单个字符）

# 第二种： 纯字符数字下划线组成的字符串， 在第一次创建时同时缓存 - 字符串驻留池
s1 = 'abc_123'
s2 = 'abc_123'
print(s1, s2, id(s1), id(s2))  # 地址相同
# 删除引用后， 对象仍 缓存 在驻留池中, 没有被销毁，可以创建新变量再次引用
del s1
del s2
s3 = 'abc_123'
print('s3', id(s3))

# 缓存机制：引用计数为零时不立马释放内存的机制， 降低频繁申请和释放内存的操作
# 对于某一个类型的数据的引用计数为零时，会从双向循环链表中移除，但是对象之前所申请的内存控件不会立即释放，会根据相关机制放入缓存中。
#  float,int; list, dict...; tuple; 其他对象
# 如是自定义对象 缓存2个对象 ： 创建了两个对象，然后调用del删除其引用。对象的内存空间被加入缓存未释放
# 再次创建两个对象，则两个新对象是用自缓存时所的记录内存地址， 重新拿来使用。
# 如是list 缓存80个对象
# 可以阅读源代码进行了解


"""==== 垃圾回收机制 ===="""
# python的垃圾回收机制用一句话来形容就是：引用计数机制为住，标记-清除和分代手机两种机制为辅的策略
# 1. 引用计数：每个对象创建之后都会有一个引用计数， 当引用计数为零的时候，那此时垃圾回收机制自动将它销毁，释放内存空间
# 引用计数存在一个缺点： 那就是当两个对象出现循环引用的时候，那这两个变量始终不会被销毁，这样会导致内存泄露
ab = [12]
cd = [34]
# 互相引用， 引用计数一直不为零
ab.append(cd)
cd.append(ab)
print(ab, cd)
del ab
del cd
print('ab', 'cd', id(ab), id(cd))

# 解决方案：
# 标记清除
# 对于所有数据内部会引用其他对象数据（如列表里套字典等），除了放在双向循环链表中

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
