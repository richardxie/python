#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

import unittest
from yatang import Cookies, Account, AccountInfo, Coupon, Invest, SigninInfo, Base
import yatang.Loan as YTLoan
import utils
import pdb, sys, os

db_name = 'test.db'
if os.path.exists(db_name):
    os.remove(db_name)

from sqlalchemy import create_engine
engine = create_engine('sqlite:///'+db_name, echo=True)
 
from sqlalchemy.orm import sessionmaker
session = sessionmaker()
session.configure(bind=engine)

Base.metadata.create_all(engine)

class TestUtils(unittest.TestCase): 
    def setUp(self):
        utils.initSys()
        pdb.set_trace()

        sys.path.append(os.path.dirname(__file__))
        pythonpath =  os.getenv('PYTHONPATH')
        if pythonpath is not None:
            paths = pythonpath.split(':' if os.name=='posix' else ';')
            for path in paths:
                if not path in sys.path:
                    sys.path.append(path)


        pass        

    def tearDown(self):
        pass

    def test_genCookie(self):
        c = Cookies("./")
        print c.genCookie("richardxiq", "root1234")
        pass 

    def test_account(self):
    	Session = sessionmaker(bind=engine)
    	session = Session()
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
        account =  Account(cookie).accountRequest()
        session.add(account)
        session.commit()
        aAccount = session.query(AccountInfo.AccountInfo).filter_by(name='richardxieq').first()
        self.assertTrue(account.name == 'richardxieq')
        self.assertTrue(account == aAccount)
        pass 

    def test_coupon(self):
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
        pdb.set_trace()
        print Coupon(cookie, '1215UQFHB020').couponListRequest()
        pass 

    def test_loan(self):
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
       	i = Invest(cookie)

        pdb.set_trace()
        print YTLoan.Loan.loanRequest(i.opener, '625994')
        pass

	def test_encryptPassword(self):
		with PyV8.JSContext() as jsctx:
			with open("encrypt.js") as jsfile:
				jsctx.eval(jsfile.read())
				encryptFunc = jsctx.locals.encrypt
				pwd = encryptFunc(password, verifyCode)
				self.assertTrue(len(pwd) > 1)
		
