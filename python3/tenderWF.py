#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from urllib.request import HTTPCookieProcessor ,build_opener,install_opener,HTTPRedirectHandler
from sched import scheduler
from time import time, sleep
from datetime import datetime,timedelta
import logging,utils,conf
from yatang import Cookies, Account, Invest, Assets, Welfare, Coupon, Loan, Session
from yatang.modules import UserInfo
from threading import Thread, current_thread

logger = logging.getLogger("app")
c = Cookies("./")
#投资秒标
class TenderWF(Thread):

    def __init__(self, user_name):
        Thread.__init__(self)
        self.username = user_name
        self.name = 'tenderThread-' + user_name
        pass

    def run(self):
        self.welfare_tender()
        pass

    def welfare_tender(self):
        session = Session()

        cj = c.readCookie(self.username)
        opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
        install_opener(opener)
        query = session.query(UserInfo).filter(UserInfo.name == self.username, UserInfo.website == 'yt')
        if query.count() == 0:
            return

        user_info = query.one() 

        for i in range(2):
            loaninfo = Welfare.walfareRequest(opener) 
            now = datetime.now()
            delta = (loaninfo.starttime - now).total_seconds()
            if delta < 0 :
                logger.warn(' 开始时间已过， 秒标投资任务未执行！%d' % delta)
                break
            elif delta > 600:
                logger.info(' 先等待%d秒后开始执行秒标投资任务！ ' % (delta - 600))
                sleep(delta - 600)
                break
            else:
                sleep(delta)
                invest = Invest(user_info.name, opener)
                invest.tenderWF(loaninfo, user_info)    
        pass
    pass

if __name__ == '__main__':
   
    #初始化
    utils.initSys()
    conf.initConfig()
    from conf import auto_tender_names
    threads = []
    for username in auto_tender_names:
        t = TenderWF(username)
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()
    
    logger.info('秒标投标任务 %s 完成.' % current_thread().name)
    