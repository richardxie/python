#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from urllib.request import HTTPCookieProcessor ,build_opener,install_opener,HTTPRedirectHandler
from sched import scheduler
from time import time, sleep
from datetime import datetime,timedelta
import logging,utils,conf
from yatang import Cookies, Account, Invest, Crowdfundings, Redpacket, Session
from yatang.modules import UserInfo
from threading import Thread, current_thread

logger = logging.getLogger("app")
c = Cookies("./")
#投资众筹
class TenderCF(Thread):
    def __init__(self, user_name, amount):
        Thread.__init__(self)
        self.user_name = user_name #投资用户名
        self.amount = amount #投资金额
        pass

    def run(self):
        self.crowdfunding_tender()
        pass

    def crowdfunding_tender(self):
        logger.debug('开始投资众筹')
        cj = c.readCookie(self.user_name)        
        #c.dumpCookies(cj)

        opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
        install_opener(opener)

        acc = Account(opener)
        accountinfo = acc.accountRequest()
        totalAmount = accountinfo.available

        session = Session()
        query = session.query(UserInfo).filter(UserInfo.name == self.user_name, UserInfo.website == 'yt')
        if query.count() == 0:
            return

        user_info = query.one()

        invest = Invest(user_info.name, opener, self.amount)
        for i in range(2):
            crowdfundings = Crowdfundings(opener)
            crowdfunding = crowdfundings.crowdfundingRequest()
            logger.info(crowdfunding)

            now = datetime.now()
            delta = (crowdfunding.starttime - now).total_seconds()
            
            if delta < 0 :
                logger.warn(' 开始时间已过， 众筹投资任务未执行！%d' % delta)
                break
            elif delta > 600:
                logger.info(' 先等待%d秒后开始执行众筹投资任务！ ' % (delta - 600))
                sleep(delta - 600)
            else:
                logger.info(' %d秒后开始执行众筹投资任务！ ' % (delta))
                sleep(delta)
                invest.tenderCF(crowdfunding, user_info)
                break

if __name__ == '__main__':
   
    #初始化
    utils.initSys()
    conf.initConfig()
    from conf import auto_tender_names
    threads = []
    for username in auto_tender_names:
        t = TenderCF(username, 4000)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
    
    logger.info('众筹投标任务 %s 完成.' % current_thread().name)
    