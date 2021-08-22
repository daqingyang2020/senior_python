#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/19 20:37
# @Author : Henry


# xx.xx的装饰器


# 算术运算符对应的魔术方法

# __add__(self, other) # a + b  , 若a + b + c ，则要确保a+b返回的对象类型和c的对象类型一致
# __sub__(self, other)


# 属性相关的魔术方法
# 1. 私有属性 __属性名

# 2. __dict__属性： 以字典的形式获取对象（类）的所有属性
class MyTest:

    name = 'Henry'
    age = 18

    def __init__(self, a):
        self.a = a


my = MyTest('new')
print(my.__dict__)
print(MyTest.__dict__)
print(dir(my))

# 3. 内置属性__slots__
li = list()
# print(li.__dict__)  # 列表无__dict__属性， 报错
print(li)
# li.name = 'Henry' # list对象不能加属性


class MySlots:
    # 限制对象可以设置的属性， 若为空， 则不能加属性
    # 加了name，则对象可以加name属性，指定了属性
    __slots__ = ['name']


sl = MySlots()
sl.name = 'Henry'
# sl.age = 18 # __slots__ 未定义此属性，报错
# 当要实例化大量对象时，__slots__限制了属性设置，节约内存
# __slots__ 限制了对象的属性， 类属性不受影响


# 自定义属性访问
# __getattr__ 没有找到属性时，出发AttributeError异常时调用
# __getattribute__ 查找属性时调用的方法 xx.xxx
# __setattr__ 设置属性触发的方法 xx.xxx = xxx
# __delattr__ 删除属性触发的方法 del xx.xxx

class Custom:
    name = "ice"


cu = Custom()
print(cu.name)
print(id(cu.name), id(Custom.name))
assert id(cu.name) == id(Custom.name)
cu.name = 'Henry'
del cu.name
print('after delete: ', cu.name)

# 定义一个类， 可以初始化name ， age两个属性
# name属性值只能是str
# age属性只能是int
# name属性不能删除
# age输出查找出来的结果少于0 则返回零


class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age


# 序列类型数据索引取值对应的魔术方法
cou = [11, 22, 33]
di = {'country': 'China', 'city': 'Shanghai'}


class String:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __getitem__(self, item):
        print('Item is:', item)
        return getattr(self, item)

    def __setitem__(self, key, value):
        print(key, value)
        setattr(self, key, value)

    def __delitem__(self, key):
        print('To delete key:', key)
        delattr(self, key)

    def __len__(self):
        """len(obj)"""
        return len(self.__dict__)


"""homework========================="""
# 属性管理
# 第一题：自定义一个列表类型，实现对象可以之间可以 使用 - 来进行操作
# # 要求：如果一个对象减去另一个对象，则把和被减对象中一样的数据给删除掉
# # 如下：
# li1 = MyList([11, 22, 33,22, 44])
# li2 = MyList([1, 22])
# res = li1 - li2
# # res 打印的结果为[11,33,44]


class MyList:

    def __init__(self, ls):
        self.ls = ls

    def __sub__(self, other):
        for item in other.ls:
            while item in self.ls:
                self.ls.remove(item)
        return self.ls
    pass


l1 = MyList([1, 2, 3, 4, 4])
l2 = MyList([3, 4])

print(l1-l2)


# 第二题、自定义一个类
#     1、通过上课的相关知识点对这个类创建的对象，进行属性限制，对象只能设置这个三个属性： title money data
#     2、通过相关机制对设置的属性类型进行限制，title只能设置字符串类型数据
#     money设置为int类型数据  data可以设置为任意类型
#     3、通过相关机制实现，data 属性不能进行删除
#     4、当money设置的值少于0时，确保查询出来的值为0，
class School:
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
