#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
import pdb, sys, os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tesserpy, cv2

from conf import db_config
from task import Financing_daily_task
import utils, PyV8
from utils.json_encoder import new_object_encoder

from yatang import Cookies, Account, Coupon, Invest, Welfare, Financing
import yatang.Loan as YTLoan
from yatang.modules import UserInfo, WelfareInfo, AccountInfo, SigninInfo, Base
from flask import json

USING_MYSQL = True

if USING_MYSQL:
    db_name = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4'%(db_config['mysql-dev']['user'],
                                                          db_config['mysql-dev']['password'],
                                                          db_config['mysql-dev']['host'],
                                                          db_config['mysql-dev']['port'],
                                                          db_config['mysql-dev']['instancename'])
else:
    db_name = 'sqlite:///%s'%(db_config['sqlite3-dev']['dbname'])

print db_name


engine = create_engine(db_name, pool_size=100, pool_recycle=3600, echo=True)
 

Session = sessionmaker()
Session.configure(bind=engine)

Base.metadata.create_all(engine)
Base.metadata.bind = engine

class TestUtils(unittest.TestCase): 
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
        print c.genCookie("richardxiq", "root1234")
        pass 

    def test_account(self):
        Session = sessionmaker(bind=engine)
        session = Session()
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
        account = Account(cookie).accountRequest()
        aAccount = session.query(AccountInfo).filter_by(name='richardxieq').first()
        self.assertTrue(account.name == 'richardxieq')
        pass 

    def test_coupon(self):
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
        print Coupon(cookie, '1215UQFHB020').couponListRequest()
        pass 

    def test_loan(self):
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
        i = Invest('richardxieq',cookie, None)
        print YTLoan.Loan.loanRequest(i.opener, {'id':'670629'})
        pass

    def test_welfare(self):
        pdb.set_trace()
        with open("backup/welfare.htm") as html:
            welfare = Welfare.welfare_info(html)
            session = Session()
            welfare_info = WelfareInfo.fromWelfare(welfare)
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

    def test_financing(self):
        c = Cookies("./")
        cookie = c.readCookie("richardxieq")
        session = Session()
        query = session.query(UserInfo).filter(UserInfo.name == 'richardxieq', UserInfo.website == 'yt')
        if query.count() == 0:
            return
            
        user_info = query.one()

        financing = Financing.Financing(name = '²âÊÔ', userId = user_info.id, cookie = cookie)

        l = financing.financingRequestPagable()
        print json.dumps(l, cls=new_object_encoder(), check_circular=False, sort_keys=True)
        pass

    def test_financing_task(self):
        task = Financing_daily_task()
        print json.dumps(task.dailyCheck(), cls=new_object_encoder(), check_circular=False, sort_keys=True)
        pass

    def test_encryptPassword(self):
        with PyV8.JSContext() as jsctx:
            with open("encrypt.js") as jsfile:
                jsctx.eval(jsfile.read())
                encryptFunc = jsctx.locals.encrypt
                pwd = encryptFunc("richard", "123")
                self.assertTrue(len(pwd) > 1)
        pass

    def test_imgRecon(self):
        import platform
        if platform.system() == 'Darwin':
            tesser = tesserpy.Tesseract('/usr/local/share/tessdata/', language="eng")
        else:
            tesser = tesserpy.Tesseract("/usr/share/tesseract-ocr/tessdata/", language="eng")
        tesser.tessedit_char_whitelist = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        #img = self.imageProcess(cv2.imread("get_captcha.jpg", cv2.IMREAD_GRAYSCALE))
        img = self.imageProcess(cv2.imread("get_captcha.jpg"))
        tesser.set_image(img);
        page_info = tesser.orientation();
        print(page_info.textline_order == tesserpy.TEXTLINE_ORDER_TOP_TO_BOTTOM)
        print("#####")
        print(tesser.get_utf8_text())
        print("#####")
        print("Word\tConfidence\tBounding box coordinates")
        for word in tesser.words():
            bb = word.bounding_box
            print("{}\t{}\tt:{}; l:{}; r:{}; b:{}".format(word.text, word.confidence, bb.top, bb.left, bb.right, bb.bottom))

    def imageProcess(self, im):
        # resize image
        enlarge = cv2.resize(im, (0, 0), fx=6, fy=6, interpolation=cv2.INTER_CUBIC)  
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(4, 4))  
        """
        im = cv2.morphologyEx(enlarge, cv2.MORPH_OPEN, kernel ) #Open and close to make appear contours
        im = cv2.morphologyEx(enlarge, cv2.MORPH_CLOSE, kernel )
        """
        im = cv2.erode(enlarge,kernel) 
        im = cv2.dilate(enlarge,kernel) 
        #im=cv2.GaussianBlur(enlarge,(5,5),0)
        thresh = 10
        maxValue = 255
        th, dst = cv2.threshold(enlarge, thresh, maxValue, cv2.THRESH_BINARY);
        cv2.imwrite('./process.png', enlarge)
        return im