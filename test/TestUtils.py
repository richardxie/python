#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

import unittest
from yatang import Cookies

class TestUtils(unittest.TestCase): 
     
    def test_genCookie(self):
        c = Cookies("./")
        print c.genCookie("richardxiq", "root1234")
        pass    