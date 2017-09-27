#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from urllib.request import HTTPCookieProcessor ,build_opener,install_opener,HTTPRedirectHandler
from sched import scheduler
from time import time, sleep
import logging,utils,conf
from yatang import Cookies, Account, Invest, Assets, Welfare, Coupon, Loan, Session
from yatang.modules import UserInfo
from threading import Thread, current_thread

logger = logging.getLogger("app")
c = Cookies("./")

#投资资产标
class Tender(Thread):
    schedule = scheduler(time, sleep) 
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name #投资人姓名
        pass

    def run(self):
        self.timming_exec()
        pass

    def timming_exec(self, inc = 20):
        self.current_event = self.schedule.enter(inc, 0, self.asset_tender, ( inc, ))
        self.tender_time = time()
        self.schedule.run()

    def asset_tender(self, inc):
        self.current_event = self.schedule.enter(inc, 0, self.asset_tender, ( inc, ))
        orginal_time = self.tender_time
        self.tender_time = time()  
        logger.debug('开始投资产标，间隔( ' + str(self.tender_time-orginal_time) + ' seconds )')
        cj = c.readCookie(self.name)        
        #c.dumpCookies(cj)

        opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
        install_opener(opener)

        acc = Account(opener)
        accountinfo = acc.accountRequest()
        totalAmount = accountinfo.available if accountinfo is not None else 0

        session = Session()
        query = session.query(UserInfo).filter(UserInfo.name == self.name, UserInfo.website == 'yt')
        if query.count() == 0:
            return

        user_info = query.one()

        invest = Invest(user_info.name, opener)
        assets = Assets(opener)
        assetList = []
        idx = 1
        while len(assetList) < 2:
            assetList.extend(assets.assetRequest(str(idx)))
            idx += 1
            if idx == 5:
                break

        print(assetList)

        for asset in assetList:
            print(asset)
            loan = Loan.loanRequest(opener, asset)
            invest.tender(loan, user_info)


if __name__ == '__main__':
   
    #初始化
    utils.initSys()
    conf.initConfig()
    from conf import auto_tender_names
    threads = []
    for username in auto_tender_names:
        t = Tender(username)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
    
    logger.info('资产投标任务 %s 完成.' % current_thread().name)