#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/21 21:13
# @Author : Henry
from unittest import TestCase
import unittest
import yaml
import json
from datetime import datetime

# 面向对象 - 封装 继承 多态（伪多态，对数据类型没有严格限制）
# 复习
"""
# 多态：python中函数的参数是没有类型限制的，所以多态在python中的体现不是很严谨。多态的概念是应用于java，c#这一类强类型语言中，而python
# 崇尚‘鸭子类型’
# 鸭子类型概念： 它并不要求严格的继承体系，关注的不是对象的类型本身，而是它是否具有要调用的方法（行为）
# 鸭子类型在python中的案例
    # 内置函数iter: 参数可以是实现迭代协议__iter__方法的任意类型对象
    # 函数len(): 调用对象的__len__魔术方法
"""


# 多继承的应用
# 定义一个api测试的用例类
#     1. 用例数据的数据
#     2. 接口请求
#     3. 响应数据提取
#     4. 断言


class HandleData:
    pass


class RequestApi:
    pass


# 基类case继承以上类，后续维护管理
class BaseTest(HandleData, RequestApi):
    def handle_data(self):
        pass

    def request_api(self):
        pass


# 元类
class MyPython:
    pass


m = MyPython()

print(type(m))  # <class '__main__.MyPython'>
print(type(MyPython))  # <class 'type'> 通过type所创建的对象
print(type('string'))
print(type([11, 22]))
print(type(dict))  # <class 'type'>
print(type(str))
print(type(list))

# python中所有的类的类型都是type， type就是元类，创建类的类
# 使用type 去创建用例类
"""
type(object_or_name, bases, dict)
type(object) -> the object's type
type(name, bases, dict) -> a new type
type 动态创建类：
    参数1：name 类名 （字符串）
    参数2：bases 继承的父类 （元组）
    参数3：dict 类的属性和方法 （字典）
"""

# 通过type定义的类, 元类一般用不到
MyNew = type('MyNew', (object,), {'name': 'henry'})
print(MyNew)
# 通过type动态生成测试类
# test_1, test_2 unittest用的测试方法，无法写测试方法逻辑
# MyTest = type('MyTest', (TestCase, ), {'cases:': [1, 2, 3],
#                                        'test_1': lambda x: x,
#                                        'test_2': lambda x: x})

# suite = unittest.defaultTestLoader.loadTestsFromTestCase(MyTest)
# unittest.main()
"""====自定义元类来实现动态创建测试类和测试方法===="""


# 生成测试类的时候，根据测试数据去动态生成测试方法
# 什么时候需要用到元类：
#     1. 动态创建类，在创建类的过程中需要自定义类属性和方法
# 需求： 自定义元类来动态创建测试类和测试方法


def test_value(funny, value):
    def inner(self, *args, **kwargs):
        result = funny(self, value, *args, **kwargs)
        return result

    return inner
    pass


# 继承元类type , class type(object) type 继承了object
class MyMateClass(type):

    # 通过类创建对象 第一参数cls 推荐写成mcs
    def __new__(mcs, name, bases, attr, *args, **kwargs):
        # 通过元类创建一个类， 调用父类的方法
        test_cls = super(MyMateClass, mcs).__new__(mcs, name, bases, attr)
        funny = getattr(test_cls, 'perform')
        # 根据传入的测试数据 参数attr ，来遍历这个属性Cases - attr['Cases']
        for index, case in enumerate(attr['Cases']):
            # 动态给test_cls这个类添加属性 - 测试方法
            # 方法使用继承自BaseApiCase中的test_perform
            method = test_value(funny, case)
            setattr(test_cls, 'test_{}'.format(index), method)
        # else: # 不能删除,继承自父类的方法属性, 修改方法名,让unittest不认为是测试方法
        #     delattr(test_cls, 'test_perform')
        # 返回测试类
        return test_cls

    pass


# 通过自定义的元类创建了一个类
# Henry = MyMateClass('Henry', (object, ), {})
# 传入的用例数据Cases， 然后根据用例数据动态生成测试方法
# Henry = MyMateClass('Henry', (unittest.TestCase, ), {'Cases': [1, 23, 13]})
#
# print()


class BaseApiCase:
    """用例执行的基类"""

    def perform(self, case):
        """用例执行方法, 接收用例数据case"""
        print('test cases:', case)
        # 1. 用例数据的处理
        # 2. 接口请求
        # 3. 响应数据提取
        # 4. 断言
        pass


# 继承unittest.TestCase， 再继承BaseApiCase 用来使用其用例测试方法
My = MyMateClass('Henry', (unittest.TestCase, BaseApiCase),
                 {'Cases': [1, 2, 33]})
print(My)
# suite = unittest.defaultTestLoader.loadTestsFromTestCase(My)
# unittest.main()

with open('case.json', 'r') as file:
    cases = json.load(file)
    # 第二种
    # result = file.read()
    # cases = json.loads(result)

print(cases)
cases_dict = dict(Cases=cases)
MyData = MyMateClass('Henry', (unittest.TestCase, BaseApiCase), cases_dict)

# yaml配置文件读取
with open('api_data.yml', 'r') as f2:
    cases2 = yaml.load(f2, Loader=yaml.SafeLoader)

print(cases2)
'''====================homework======================'''


# 1、自定义一个元类，可以在创建类的时候，自动给类添加（class_name,create_time）
# 这两个类属性，属性值自己随便写一个
class Custom(type):
    def __new__(mcs, name, bases, attr):
        my_cls = super(Custom, mcs).__new__(mcs, name, bases, attr)
        setattr(my_cls, 'class_name', name)
        setattr(my_cls, 'create_time', datetime.today())
        return my_cls


Peter = Custom('Peter', (object, ), {})
print(getattr(Peter, 'class_name'))
print(getattr(Peter, 'create_time'))

# 2、实现上课写的通过元类生成用例的案例代码
# 见上

"""
说明：以下面试扩展算法题，和上课内容无关，不计分，不是必做题
扩展1：
有一艘船上有40个人，由于触礁出现了漏水，现在船上最多只能载20个人，需要20个人下船。
于是这40个人排成一队，根据站位，每个人领取了一个编号，从1开始到40。
然后从1开始到9进行循环报数，报数为9的人出列下船，一直循环，直到船上只剩下20人。
示例：1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19....40
第一次报到9下船的人，编号为9（1,2,3,...编号为9的人报9）
第二次下船的，编号为18，（10的人报1....18的人报9）
第三次下船的，编号为27  （19的人报1....27的人报9）
第四次下船，编号为36  （28的人报1....36的人报9）
第五次下船，编号为5 （37的人报1，38报2,39报3,40报4....5的人报9）
第六次下船，编号为15
.....
请问最后那些编号的人下船了？
"""

people = [person for person in range(1, 41)]
print(people)
# 离开的人
leave = []
# 初始化第九人
index = 8
# 越界
over = 0
while len(people) > 20:
    while index <= len(people):
        one = people.pop(index)
        leave.append(one)
        cur_len = len(people)
        if cur_len == 20:
            break
        index += 8
        if index >= cur_len:
            # 越界
            over = index - cur_len
            break
        else:
            pass
    # 越界后重置
    index = over
print('Total Leave people:', len(leave))
print(leave)

#
people = [person for person in range(1, 41)]


def leave_people(remain):
    take_off = []
    flag = 8
    while len(remain) > 20:
        each = people.pop(flag)
        take_off.append(each)
        current_len = len(remain)
        if current_len == 20:
            break
        if flag + 8 >= current_len:
            flag = flag + 8 - current_len
        else:
            flag += 8
    return take_off


print('use function:')
ll = leave_people(people)
print(ll, len(ll))


"""
扩展2：
2 一个球从100米高度自由落下，每次落地后反跳回原高度的一半；再落下，
求它在第10次落地时，共经过多少米？请用递归实现！
次数                                    
1    100
2    100                               +     (100/2)*2    100        100/2**(0)         
3    100+100/2*2                       +     (100/4)*2    100/2      100/2**(1)
4    100+100/2*2+100/2*2               +     (100/8)*2    100/4      100/2**(2)
5    100+100/2*2+100/2*2+100/2*2*2     +     (100/16)*2   100/8      100/2**(3)
n    上一次的累计距离   +                 +                             (100/2**(n-2))
"""


def fall(height, times):
    if times == 1:
        return height
    else:
        # n次 = 上一次的累计距离 + (高度/2**(n-2))
        return fall(height, times-1) + height / 2**(times-2)
    pass


print('The ball has gone:', fall(100, 10))

"""
扩展3
问题：小明有一对刚出生的兔子，兔子的成长期为2个月，从第三个月开始每个月都生一对小兔子，
子，假如兔子都不小兔子从第三个月开始每个月也会生一对兔死，问n个月后的兔子总数为多少？请用递归实现（意味着生长期为2个月）

1   --->   2                                                         2    1
2   --->   2                                                         2    1
3   --->   2 + 2(新生一对)                                             4    2
4   --->   4 + 2(新生一对)                                             6    3
5   --->   6 + 2(新生一对) +2(3月份的也新生一对)                          10    5
6   --->   8 + 2(新生一对) +2(3月份的也新生一对) +2(4月份的也新生一对)       16    8
                                                                     26     13
                                                                     42    21

"""


def rabbit(month):
    if month == 1 or month == 2:
        return 2
    else:
        return 2 * (month-2) + rabbit(month-2)
    pass


print('There are rabbits:', rabbit(6))

# 扩展4：有时间的小伙伴 可以尝试利用讲的元类的思想 自己封装测试框架

