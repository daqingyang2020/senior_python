#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/10/17 
# @Author  : henry
# @File    : exercise_8.py
from datetime import datetime


# 1、自定义一个元类，可以在创建类的时候，自动给类添加（class_name,create_time）
# 这两个类属性，属性值自己随便写一个
class Custom(type):
    def __new__(mcs, name, bases, attr):
        my_cls = super(Custom, mcs).__new__(mcs, name, bases, attr)
        setattr(my_cls, 'class_name', name)
        setattr(my_cls, 'create_time', datetime.today())
        return my_cls


Peter = Custom('Peter', (object,), {})
print(getattr(Peter, 'class_name'))
print(getattr(Peter, 'create_time'))

# 2、实现上课写的通过元类生成用例的案例代码
# 见上课代码

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
        return fall(height, times - 1) + height / 2 ** (times - 2)
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
        return 2 * (month - 2) + rabbit(month - 2)
    pass


print('There are rabbits:', rabbit(6))

# 扩展4：有时间的小伙伴 可以尝试利用讲的元类的思想 自己封装测试框架
