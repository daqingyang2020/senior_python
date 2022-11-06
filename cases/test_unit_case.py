#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021/9/2 
# @Author  : henry
# @File    : test_unit_case.py
import unittest
from time import sleep


class TestTerminal(unittest.TestCase):

    def test_one(self):
        print('Test one')
        sleep(0.3)
        assert 1 == 1

    def test_two(self):
        print('Test tow')
        sleep(0.3)
        assert 1 != 2

    def test_three(self):
        print('Test three')
        sleep(0.3)
        assert 2 == 2
