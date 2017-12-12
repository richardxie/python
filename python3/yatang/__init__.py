#!/usr/bin/python3.6
# ！-*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.dirname(__file__))

from Cookies import Cookies
from Login import Login
from Account import Account
from Assets import Assets
from Welfare import Welfare
from Coupon import Coupon
from Invest import Invest
from Crowdfundings import Crowdfundings
from Redpacket import Redpacket
from GrabTicketCash import GrabTicketCash
from RedEnvelope import GradRedPacket
from modules import AccountInfo
from Loan import Loan
from modules import InvestInfo
from modules import Base
from conf import db_config


YTURLBASE = "http://jr.yatang.cn/"
YTURLBASESSL = "https://jr.yatang.cn/"
YTAPIBASESSL = "https://yztapi.yatang.cn/"
YT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'

USE_MYSQL = False
if USE_MYSQL:
    db_name = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4'%(db_config['mysql']['user'],
                                                          db_config['mysql']['password'],
                                                          db_config['mysql']['host'],
                                                          db_config['mysql']['port'],
                                                          db_config['mysql']['instancename'])
else:
    db_name = 'sqlite:///%s'%(db_config['sqlite3']['dbname'])


from sqlalchemy import create_engine
if USE_MYSQL:
    engine = create_engine(db_name, pool_size=100, pool_recycle=3600, echo=True)
else:
    engine = create_engine(db_name, echo=True)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

reserved_amount = 5000
SUPPLY_CHAIN_BID = '1' #供应链金融标
WELFARE_BID = '5' #秒标
def borrowTypeName(borrowType):
    names = {
            '1':'供应链金融标 - 企业标'
            ,'5':'秒标-开心利是'
            ,'6':'净值标-资产一号'
            ,'7':'净值标-资产二号'
            ,'9':'供应链金融标-创业标'
            ,'10':'股权净值标-资产四号'
            } 
    return names[borrowType]

def repayTypeName(repayStyle):
    names = {
            '4':'按天到期'
            ,'0':'按月分期'
            } 
    return names[repayStyle]