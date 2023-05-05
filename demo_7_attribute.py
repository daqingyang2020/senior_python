#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/19 20:37
# @Author : Henry

# xx.xx的装饰器
# 装饰器扩展 @xxx.yyy.zzz - 模块.对象.方法
# 模块中定义类，对象方法为装饰器函数，模块中实例化类对象

# __str__方法
class MyTest:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'MyTest - {}'.format(self.name)


m1 = MyTest('Henry')
print(m1)  # 未重定义__str__默认打印： <__main__.MyTest object at 0x000001DE2497A588>


# 算术运算符对应的魔术方法

# __add__(self, other) # a + b  , 若a + b + c ，则要确保a+b返回的对象类型和c的对象类型一致
# __sub__(self, other)
class MyAdd:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        # self 自身对象，other 另一个对象（同类型）
        return self.value + other.value


m1 = MyAdd(11)
m2 = MyAdd(22)

print(m1 + m2)  # 触发__add__方法，数值相加


# 属性相关的魔术方法
# 1. 私有属性 __属性名

# 2. __dict__属性： 以字典的形式获取对象（类）的所有属性
class MyTest:
    name = 'Henry'
    age = 18

    def __init__(self, word):
        self.word = word


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
    # __slots__限制类的对象可以设置的属性， 若为空， 则不能加属性， 同样没有__dict__属性
    __slots__ = ['name']  # 加了name，则对象可以加name属性，指定了属性，不能加其他属性


sl = MySlots()
sl.name = 'Henry'


# sl.age = 18 # __slots__ 未定义此属性，报错
# 当要实例化大量对象时，__slots__限制了属性设置 如__dict__，节约内存
# __slots__ 限制了对象的属性， 类属性不受影响


# 自定义属性访问
# __getattr__ 没有找到属性时，出发AttributeError异常时调用
# __getattribute__ 查找属性时调用的方法 xx.yy / getattr(xx, yy)
# __setattr__ 设置属性触发的方法 xx.yy = zz /  setattr(xx, yy, zz)
# __delattr__ 删除属性触发的方法 del xx.yy  / delattr(xx, yy)

class Custom(object):
    name = "ice"

    # 查找属性的魔术方法 - xx.yy / getattr(xx, yy)， 接收的参数item，即属性名
    def __getattribute__(self, item):
        print('查找属性时，首先会进入该方法')
        # 返回属性值
        return super(Custom, self).__getattribute__(item)

    # 没有找到属性时会触发这个魔术方法
    def __getattr__(self, item):
        print('没有找到属性时， 触发AttributeError异常时会调用此方法')
        # 可以返回一个默认值
        return 'Pycharm'

    # xx.yy = zz / setattr(xx, yy, zz) 设置属性时调用的方法
    def __setattr__(self, key, value):
        print('设置属性，会调用此方法')
        super(Custom, self).__setattr__(key, value)

    # 删除属性时触发的魔术方法
    def __delattr__(self, item):
        print('属性被删除了')
        super(Custom, self).__delattr__(item)


cu = Custom()
print(cu.name)  # 对象.属性 - 触发了魔术方法 __getattribute__
print(getattr(cu, 'name'))
print(cu.age)  # 对象.属性 - 属性没有找到时，产生AttributeError异常，触发了魔术方法 __getattr__
cu.name = 'Henry'
del cu.name

print(id(cu.name), id(Custom.name))
assert id(cu.name) == id(Custom.name)

print('after delete: ', cu.name)

"""自定义属性访问举例"""
# 定义一个类， 可以初始化name ，age两个属性
# 1.name属性值只能是str
# 2.age属性只能是int
# 3.name属性不能删除
# 4.age输出查找出来的结果少于0 则返回零


class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __setattr__(self, key, value):
        if key == 'name':
            if isinstance(value, str):
                super(MyClass, self).__setattr__(key, value)
            else:
                raise TypeError('name属性值只能是字符串')
        elif key == 'age':
            if isinstance(value, int):
                super(MyClass, self).__setattr__(key, value)
            else:
                raise TypeError('age属性值只能是整数')
        else:
            super(MyClass, self).__setattr__(key, value)


# 序列类型数据索引取值对应的魔术方法
cou = [11, 22, 33]
di = {'country': 'China', 'city': 'Shanghai'}


class String:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    # 实现索引取值的魔术方法 - x[y]
    def __getitem__(self, item):
        print('item', item)
        # 返回对象的属性值
        return getattr(self, item)

    # 设置索引的魔术方法 - x[y] = z
    def __setitem__(self, key, value):
        print(key, value)
        setattr(self, key, value)

    # 删除索引的魔术方法 - del x[y]
    def __delitem__(self, key):
        print('To delete key删除索引:', key)
        delattr(self, key)

    # 获取对象数据的长度魔术方法 - len(x)
    def __len__(self):
        """len(obj)"""
        return len(self.__dict__)


s = String('1', '2', '3', '4')
print(s['a'])

s['e'] = '5'
print(s['e'])
del s['a']
print(s.__dict__)
print(len(s))
