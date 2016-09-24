#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from Cookies import Cookies
from Signin import Signin
from Invest import Invest
from Welfare import Welfare
from Coupon import Coupon
from Account import Account
from modules import AccountInfo
from modules import InvestInfo
from modules import Base
from os import path

YTURLBASE = "http://jr.yatang.cn/"
YTURLBASESSL = "https://jr.yatang.cn/"
YT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'

db_name = 'test.db'

from sqlalchemy import create_engine
engine = create_engine('sqlite:////usr/src/vagrant'+db_name, echo=True)
	 
from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)
if not path.exists(db_name):
	Base.metadata.create_all(engine)