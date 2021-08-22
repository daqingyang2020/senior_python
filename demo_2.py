#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/7 20:57
# @Author : Henry
#
# from collections import namedtuple
#
# # 命名元组
# Student = namedtuple('Student', ['name', 'age', 'gender'])
#
# print(Student)
#
# henry = Student('henry', 18, 'male')
#
# print(henry)
# print(henry[2])
# print(henry.name)
#
#
# # ************ 推导式 ************
# # 列表推导式 --- 快速生成列表
# list_1 = ['data{}'.format(i) for i in range(100)]
# print(list_1)
#
# # 列表推导式结合if语句进行过滤
# list_2 = ['day{}'.format(i) for i in range(100) if i % 2 == 0]
# print(list_2)
#
# #  列表推导式结合三目运算符的使用
# # 三目运算符
# n = 3
# result = 'ok' if n > 5 else 'not ok'
#
# list_3 = ['even' if i % 2 == 0 else 'odd' for i in range(100)]
# print(list_3)
#
# # ***********字典推导式*******************
# # 基本字典推导式
# dict_1 = {'key{}'.format(i): i for i in range(10)} # type 'dict'
# print(dict_1)
# # 同样可以结合if ，或者三目运算符
#
#
# # 拓展***集合推导式
# set_1 = {'key{}'.format(i) for i in range(10)} # type 'set'
# print(set_1)
#
# # 将如下字符串转换为字典格式的数据
# cook_str = ' build=D2323;pstm=15621 '
# dict_2 = {}
# res = cook_str.split(';')
# for item in res:
#     data = item.strip().split('=')
#     print(data)
#     dict_2[data[0]] = data[1]
# print(dict_2)
#
# dict_3 = {item.strip().split('=')[0]: item.strip().split('=')[1] for item in cook_str.split(';')}
# print(dict_3)
#
# # 推导式的双重for循环 --- item 一层for循环， i 二层for循环 对item再循环处理 （了解，应用不多）
# dict_4 = {i for item in cook_str.split(';') for i in item.split('=')}
# print(dict_4)
#
#
# # 生成器表达式
# # 节约内存， 产生generator对象保存数据生成的规则
# generator = (i for i in range(100))
# print(generator)
#
# for i in generator:
#     print(i, end=',')


# 推导式的练习
# 1、通过列表推导式完成下面数据类型转换
# 现在有以下数据， li1 = ["{'a':11,'b':2}", "[11,22,33,44]"]
# 需要转换为以下格式： li1 = [{'a': 11, 'b': 2}, [11, 22, 33, 44]]
li1_init = ["{'a':11,'b':2}", "[11,22,33,44]"]
li1 = [eval(li1_init[i]) for i in range(2)]
print(li1)
# 2、 Names = ['python', 'java', 'php', 'c', 'c++', 'django', 'unittest', 'pytest',
#             'pymysql'], 请通过列表推导式，获取names中字符串长度大于4的元素
names = ['python', 'java', 'php', 'c', 'c++', 'django', 'unittest', 'pytest',
         'pymysql']
filter_name = [item for item in names if len(item) > 4]
print(filter_name)
# 3、通过字典推导式，颠倒字典的键名和值:
# 将 {'py': "python09", 'java': "java09"} 转换为： {'python09': "py", 'java09': "java"}
dict_0 = {'py': "python09", 'java': "java09"}
dict_new = {dict_0[key]: key for key in dict_0}
print(dict_new)
# 4、将字典
# {'x': 'A', 'y': 'B', 'z': 'C'}
# 通过推导式转换为：['x=A', 'y=B', 'z=C']
dict_2 = {'x': 'A', 'y': 'B', 'z': 'C'}
li2 = ['{}={}'.format(a, dict_2[a]) for a in dict_2.keys()]
print(li2)
