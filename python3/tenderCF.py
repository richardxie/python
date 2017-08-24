#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from urllib.request import HTTPCookieProcessor ,build_opener,install_opener,HTTPRedirectHandler
from sched import scheduler
from time import time, sleep
from datetime import datetime,timedelta
import logging,utils,conf
from yatang import Cookies, Account, Invest, Crowdfundings, Redpacket, Session
from yatang.modules import UserInfo

logger = logging.getLogger("app")
c = Cookies("./")
#投资众筹
class TenderCF:
    def __init__(self):
        pass

    def crowdfunding_tender(self):
        logger.debug('开始投资众筹')
        cj = c.readCookie('richardxieq')        
        #c.dumpCookies(cj)

        opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
        install_opener(opener)

        acc = Account(opener)
        accountinfo = acc.accountRequest()
        totalAmount = accountinfo.available

        session = Session()
        query = session.query(UserInfo).filter(UserInfo.name == "richardxieq", UserInfo.website == 'yt')
        if query.count() == 0:
            return

        user_info = query.one()

        invest = Invest(user_info.name, opener)
        crowdfundings = Crowdfundings(opener)
        crowdfunding = crowdfundings.crowdfundingRequest()
        logger.info(crowdfunding)

        now = datetime.now()
        delta = (crowdfunding.starttime - now).total_seconds()
        
        if delta < 0 :
            logger.warn(' 开始时间已过， 众筹投资任务未执行！%d' % delta)
        else:
            logger.info(' %d秒后开始执行众筹投资任务！ ' % (delta))
            sleep(delta)
            invest.tenderCF(crowdfunding, user_info)

if __name__ == '__main__':
   
    #初始化
    utils.initSys()
    conf.initConfig()
    TenderCF().crowdfunding_tender()