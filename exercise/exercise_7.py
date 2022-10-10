#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/10/10 
# @Author  : henry
# @File    : exercise_7.py

# 属性管理
# 第一题：自定义一个列表类型，实现对象可以之间可以 使用 - 来进行操作
# # 要求：如果一个对象减去另一个对象，则把和被减对象中一样的数据给删除掉
# # 如下：
# li1 = MyList([11, 22, 33,22, 44])
# li2 = MyList([1, 22])
# res = li1 - li2
# # res 打印的结果为[11,33,44]

# 实现方法一
# class MyList:
#
#     def __init__(self, ls):
#         self.ls = ls  # 初始化列表
#
#     # 实现减法运算符的魔术方法
#     def __sub__(self, other):
#         for item in other.ls:
#             while item in self.ls:
#                 self.ls.remove(item)
#         return self.ls

# 实现方法二
class MyList(list):

    # 实现减法运算符的魔术方法
    # def __sub__(self, other):
    #     new_list = []
    #     for item in self:
    #         if item not in other:
    #             new_list.append(item)
    #     return new_list

    def __sub__(self, other):
        # 实现方法三 列表推导式实现
        new_list = [item for item in self if item not in other]
        return new_list


l1 = MyList([1, 2, 3, 4, 4])
l2 = MyList([3, 4])

print(l1 - l2)


# 第二题、自定义一个类
#     1、通过上课的相关知识点对这个类创建的对象，进行属性限制，对象只能设置这个三个属性： title money data
#     2、通过相关机制对设置的属性类型进行限制，title只能设置字符串类型数据
#     money设置为int类型数据  data可以设置为任意类型
#     3、通过相关机制实现，data 属性不能进行删除
#     4、当money设置的值少于0时，确保查询出来的值为0，
class School(object):  # 继承父类object
    # 属性限制
    __slots__ = ['title', 'money', 'data']

    def __init__(self, title='university', money=100, data='Shanghai'):
        self.title = title
        self.money = money
        self.data = data

    def __delattr__(self, item):
        # print('To delete the item：', item)
        if item == 'data':
            raise ValueError('Can not delete data property')
        else:
            # 不能调用delattr, 否则还是回到__delattr__，死循环
            # object.__delattr__(self, item) 通过父类类名调用
            super(School, self).__delattr__(item)

        pass

    def __setattr__(self, key, value):
        # print('Set the attribute:', key, 'as', value)
        if key == 'title' and not isinstance(value, str):
            raise TypeError('Title should be a string')
        elif key == 'money' and not isinstance(value, int):
            raise TypeError('Money should be integer')
        else:
            # self.title = value  # 调用 自己的__setattr__, 死循环
            # setattr(self, key, value)  # 调用 自己的__setattr__, 死循环
            # 使用父类方法设置
            super(School, self).__setattr__(key, value)
            # print('Success')

    def __getattribute__(self, item):
        # 调用父类方法可以通过super()调用，也可以通过父类名调用其方法
        # result = object.__getattribute__(self, item)  # 通过父类名调用实例方法时，需要传递实例对象
        result = super(School, self).__getattribute__(item)
        if item == 'money' and result < 0:
            return 0
        else:
            return result


un = School()
print(un.title)
print(un.money)
# del un.data  # raise ValueError
print(un.data)
# un.title = []  # raise TypeError
# setattr(un, 'money', 12.2) # raise TypeError
setattr(un, 'money', -12)
print(un.money)
del un.money
