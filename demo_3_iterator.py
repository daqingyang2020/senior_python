#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/10 20:31
# @Author : Henry
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Generator


# 可迭代对象
class MyList:
    # 自定义的可迭代对象类
    def __iter__(self):
        # 内置函数 iter  - 返回迭代器
        return iter([11, 22, 33])


class MySequence:
    # 自定义的序列类

    def __getitem__(self, num):
        #  索引取值 num是传入的索引值 对象使用索引取值表达式时如：item[0], 即调用此方法
        # 可进行for语句迭代
        print('number:', num)


m = MyList()
print(isinstance(m, Iterable))
# m对象实现了__iter__方法(返回迭代器对象)，则是一个可迭代对象，可进行for语句迭代 for item in m:

s = MySequence()
# （实现了此方法__getitem__的对象被称为可迭代对象-支持迭代操作，但不是Iterable类型）
print(isinstance(s, Iterable))

dd = {'name': 'Henry', 'age': '20'}
# 对字典取key:
# dd.keys(), Iterable  # 是可迭代对象
# dd.keys(), not Iterator  # 不是迭代器
# iter(dd.keys()), Iterator  # 通过iter()来转换成迭代器 - 则实现了对其使用next()方法


li1 = iter([11, 22, 33, 44, 55])
print(li1.__length_hint__())  # 可迭代对象内部包含的数据数量。每次迭代后，长度减一
# 可以使用next(li1) 进行迭代，或者 li1.__next__() 进行迭代
print(li1.__setstate__(2))  # 设置迭代操作时的迭代起始位置， 默认0
print(li1.__next__())

with open('demo_2_comprehensions.py', 'r', encoding='utf-8') as file:
    res = iter(file.readlines())  # 大文件读取通过迭代器

print(res)
print(next(res))

"""
1. 可迭代对象 （了解概念）
2. 迭代器 （1 如何将可迭代对象转换未迭代器， 2 掌握使用next进行迭代操作）
3. 生成器：
    1. 定义生成器： 
        - 生成器表达式
        - 生成器函数: 在函数中使用yield关键字来实现
    2. 生成器的迭代操作（生成数据）
        - 内置函数next()
    3. 和生成器内部数据交互:
        - send方法可以往生成器内部传递数据
    4. close(): 关闭生成器--- 之后不能再next()
    5. throw(): 主动往生成器内部抛出异常-- 相当于在生成器内部执行raise 语句 --- 基本不用。
    
"""

#  生成器表达式
gen_1 = (i for i in range(10))
# 使用next 进行迭代（生成数据）
print(next(gen_1))
print(next(gen_1))
# 使用for循环进行迭代
for j in gen_1:
    print(j)


# 生成器函数：关键字yield
def func_1():
    print('start')
    yield 5
    print('continue')
    yield 10
    print('end')


# 1 使用next()对生成器进行迭代操作
# 调用生成器函数， 创建生成器对象
gen_2 = func_1()
# 调用一次next() , 进入函数执行，遇到yield暂停返回数据
# 再次调用next(), 继续从上次yield处继续执行，如此循环
# 调用next()后，若函数执行完毕后而未遇到yield，则会引发StopIteration - pytest的fixture函数在yield返回后进行执行代码（后置代码）
print(next(gen_2))
print(next(gen_2))


# print(next(gen_2))

# next(gen_2)

#  生成器的特殊方法
def func_01():
    for i in range(20):
        yield i


g1 = func_01()

print(next(g1))


# 2 使用send方法使用迭代 , 第二种迭代方法
def func_2():
    for i in range(100):
        out = yield i
        print('out:', out)


# 先使用next()启动生成器
# 再使用send()方法， 从yield开始执行， send的值可以通过yield表达式前的变量来接收 out = yield i
# 调用send的返回值是 yield后的值
gen_3 = func_2()
next(gen_3)
res = gen_3.send(123)
print('res:', res,
      'next:', next(gen_3))


# demo ---  生成一个 {'data': 'xxx'} 的生成器 xxx是传入的数据
def demo_data():
    resp = {'data': None, 'title': None}
    for i in range(10, 13):
        send_value = yield resp  # 返回内部定义的值, 在迭代完成（函数执行完成）之前，变量一直保存在内存中，
        resp.update(data=send_value)
        resp.update(title=str(i))


gg = demo_data()
print(next(gg))
print(gg.send('Henry'))

#  =============迭代器生成器作业=================
"""
1、现在有一个列表   li = [11,21,4,55,6,67,123,54,66,9,90,56,34,22], 
请将 大于5的数据过滤出来，然后除以2取余数，结果放到一个生成器中

2、定义一个可以使用send传入域名，自动生成一个在前面加上http://，在后面加上路径/user/login的url地址，
生成器最多可以生成5个url,生成5条数据之后再去生成，则报错StopIteration
使用案例：
# 例如:
res = g.send('www.baidu.com')
# 生成数据res为：http://www.baidu.com/user/logim'

3、面试笔试扩展题
有一个正整数列表(数据是无序的,并且允许有相等的整数存在),
编写一个能实现下列功能的函数，传入列表array,和正整数X，返回下面要求的2个数据
def func(array, x)
    '''逻辑代码'''
    return count, li
1、统计并返回在列表中,比正整数x大的数有几个(相同的数只计算一次)，并返回-----返回值中的的count
2、计算列表中比正整数X小的所有偶数，并返回  -----------返回值中的li
"""
# 1.
li1 = [11, 21, 4, 55, 6, 67, 123, 54, 66, 9, 90, 56, 34, 22]
gen_li = (item % 2 for item in li1 if item > 5)


# 2.
def add_url():
    ahead = 'http://'
    api = '/user/login'
    domain = yield
    for i in range(5):
        url = ahead + domain + api
        domain = yield url


gen_url = add_url()
next(gen_url)
print(gen_url.send('www.baidu.com'))
print(gen_url.send('www.google.com'))
print(gen_url.send('www.tencent.com'))
print(gen_url.send('www.126.com'))
print(gen_url.send('www.163.com'))


# gen_url.send('www.yahoo.com')


# 3.
# def func(array, x):
#     count = 0
#     li = []
#     new_array = []
#     for i in array:
#         if i > x:
#             if i in new_array:
#                 continue
#             else:
#                 count += 1
#                 new_array.append(i)
#         elif i % 2 == 0:
#             li.append(i)
#     return count, li
def func(array, x):
    count = [y for y in set(array) if y > x]
    li = [i for i in array if i < x and i % 2 == 0]
    return len(count), li


print(func([8, 2, 1, 5, 6, 6], 3))

print(3200 * (1 - 1 / 1277 * 204))
