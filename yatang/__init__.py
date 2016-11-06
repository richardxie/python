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
from conf import db_config

YTURLBASE = "http://jr.yatang.cn/"
YTURLBASESSL = "https://jr.yatang.cn"
YT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
USING_MYSQL = True
SIGNIN = True

if USING_MYSQL:
    db_name = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4'%(db_config['mysql-dev']['user'],
                                                          db_config['mysql-dev']['password'],
                                                          db_config['mysql-dev']['host'],
                                                          db_config['mysql-dev']['port'],
                                                          db_config['mysql-dev']['instancename'])
else:
    db_name = 'sqlite:///%s'%(db_config['sqlite3']['dbname'])

from sqlalchemy import create_engine
engine = create_engine(db_name, pool_size=100, pool_recycle=3600, echo=True)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

import os, sys
sys.path.append(os.path.dirname(__file__))

SUPPLY_CHAIN_BID = '1' #供应链金融标
WELFARE_BID = '5' #秒标
def borrowTypeName(borrowType):
	names = {
			'1':'供应链金融标 - 企业标'
			,'5':'秒标-开心利是'
			,'6':'净值标-资产一号'
			,'7':'净值标-资产二号'
			,'9':'供应链金融标 - 创业标'
			} 
	return names[borrowType];