#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from urllib.request import HTTPCookieProcessor ,build_opener,install_opener,HTTPRedirectHandler
from sched import scheduler
from time import time, sleep
import logging,utils,conf
from yatang import Cookies, Account, Invest, Supplychains, Loan, Session
from yatang.modules import UserInfo

logger = logging.getLogger("app")
c = Cookies("./")

#投资供应链标
class TenderSC:
    schedule = scheduler(time, sleep) 
    def __init__(self, name):
        self.name = name #投资人姓名
        pass

    def timming_exec(self, inc = 20):
        self.current_event = self.schedule.enter(inc, 0, self.supplychain_tender, ( inc, ))
        self.tender_time = time()
        self.schedule.run()

    def supplychain_tender(self, inc):
        self.current_event = self.schedule.enter(inc, 0, self.supplychain_tender, ( inc, ))
        orginal_time = self.tender_time
        self.tender_time = time()  
        logger.debug('开始投供应链标，间隔( ' + str(self.tender_time-orginal_time) + ' seconds )')
        cj = c.readCookie(self.name)        
        #c.dumpCookies(cj)

        opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
        install_opener(opener)
        
        acc = Account(opener)
        accountinfo = acc.accountRequest()
        totalAmount = accountinfo.available

        session = Session()
        query = session.query(UserInfo).filter(UserInfo.name == self.name, UserInfo.website == 'yt')
        if query.count() == 0:
            return

        user_info = query.one()

        invest = Invest(user_info.name, opener)
        supplychains = Supplychains(opener)
        scList = supplychains.supplyChainRequest()
        for sc in scList:
            loan = Loan.loanRequest(opener, sc)
            invest.tender(loan, user_info)


if __name__ == '__main__':
   
    #初始化
    utils.initSys()
    conf.initConfig()
    TenderSC("emmaye").timming_exec()