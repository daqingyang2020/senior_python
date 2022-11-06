#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2022/11/2 
# @Author  : henry
# @File    : test_unit_2.py
import unittest
from ddt import ddt, data
from time import sleep


class TestEmulator(unittest.TestCase):

    def test_1(self):
        print('Test 1')
        sleep(0.3)
        assert 1 == 1

    def test_2(self):
        print('Test 2')
        sleep(0.3)
        assert 2 == 2

    def test_3(self):
        print('Test 3')
        sleep(0.3)
        assert 2 == 2


@ddt
class TestArcher(unittest.TestCase):
    @data(3, 4, 5)
    def test_archer(self, case):
        sleep(case * 0.1)
        print(case ** 2)
