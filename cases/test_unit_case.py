#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/9/2 
# @Author  : henry
# @File    : test_unit_case.py
import unittest
from time import sleep


class Terminal(unittest.TestCase):

    def testone(self):
        print('Test one')
        sleep(0.3)
        assert 1 == 1

    def testtwo(self):
        print('Test tow')
        sleep(0.3)
        assert 1 == 2

    def testthree(self):
        print('Test three')
        sleep(0.3)
        assert 2 == 2


class Emulator(unittest.TestCase):

    def test1(self):
        print('Test 1')
        sleep(0.3)
        assert 1 == 1

    def test2(self):
        print('Test 2')
        sleep(0.3)
        assert 2 == 2

    def test3(self):
        print('Test 3')
        sleep(0.3)
        assert 2 == 2
