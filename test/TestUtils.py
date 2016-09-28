#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

import unittest
from yatang import Cookies, Account, Coupon, Invest, Welfare
import yatang.Loan as YTLoan
from yatang.modules import WelfareInfo, AccountInfo, SigninInfo, Base
from datetime import datetime
from conf import db_config
import utils, PyV8
import pdb, sys, os

USING_MYSQL = True

if USING_MYSQL:
    db_name = 'mysql+pymysql://%s:%s@%s:%s/%s'%(db_config['mysql']['user'],
                                                          db_config['mysql']['password'],
                                                          db_config['mysql']['host'],
                                                          db_config['mysql']['port'],
                                                          db_config['mysql']['instancename'])
else:
    db_name = 'sqlite:///%s'%(db_config['sqlite3-dev']['dbname'])

print db_name

from sqlalchemy import create_engine
engine = create_engine(db_name, echo=True)
 
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)

Base.metadata.create_all(engine)
Base.metadata.bind = engine

class TestUtils(unittest.TestCase): 
    def setUp(self):
        utils.initSys()
        pdb.set_trace()
        
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
        print c.genCookie("richardxiq", "root1234")
        pass 

    def test_account(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
        account = Account(cookie).accountRequest()
        session.add(account)
        session.commit()
        aAccount = session.query(AccountInfo).filter_by(name='richardxieq').first()
        self.assertTrue(account.name == 'richardxieq')
        self.assertTrue(account == aAccount)
        pass 

    def test_coupon(self):
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
        print Coupon(cookie, '1215UQFHB020').couponListRequest()
        pass 

    def test_loan(self):
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
        i = Invest(cookie)

        print YTLoan.Loan.loanRequest(i.opener, '625994')
        pass

    def test_welfare(self):
        pdb.set_trace()
        with open("backup/welfare.htm") as html:
            welfare = Welfare.welfare_info(html)
            session = Session()
            welfare_info = WelfareInfo(
                        ibid = welfare.ibid,                          
                        borrowType=welfare.borrowType,
                        borrowNum=welfare.borrowNum
                    )
            session.add(welfare_info)
            session.commit()
        pass

    def test_signin(self):
        session = Session()
        query = session.query(SigninInfo).filter(SigninInfo.name == 'richardxieq')
        if(query.count() == 0):
            import uuid
            signin_info = SigninInfo(
                            id=str(uuid.uuid1()),
                            name='richardxieq',
                            website='yt'
                        )
            session.add(signin_info)
            session.commit()
        else:
            signin_info = query.one();
            signin_info.prev_signin_date = signin_info.signin_date
            signin_info.signin_date = datetime.now()
            session.commit()
        self.assertTrue(signin_info.name == "richardxieq")
        pass

    def test_encryptPassword(self):
        with PyV8.JSContext() as jsctx:
            with open("encrypt.js") as jsfile:
                jsctx.eval(jsfile.read())
                encryptFunc = jsctx.locals.encrypt
                pwd = encryptFunc("richard", "123")
                self.assertTrue(len(pwd) > 1)
        pass
