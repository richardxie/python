#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import unittest
import utils
from datetime import datetime
import pdb, sys, os

from yatang import Cookies

class test_cookie(unittest.TestCase): 
    def setUp(self):
        utils.initSys()
        
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
        
        pythonpath = os.getenv('PYTHONPATH')
        if pythonpath is not None:
            paths = pythonpath.split(':' if os.name == 'posix' else ';')
            for path in paths:
                if not path in sys.path:
                    sys.path.append(path)


        pass        

    def tearDown(self):
        pass

    def test_genCookie(self):
        c = Cookies("./")
        print(c.genCookie("richardxiq", "root1234"))
        pass 

if __name__ =='__main__':  
    unittest.main()  