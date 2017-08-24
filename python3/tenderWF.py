#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from urllib.request import HTTPCookieProcessor ,build_opener,install_opener,HTTPRedirectHandler
from sched import scheduler
from time import time, sleep
import logging,utils,conf
from yatang import Cookies, Account, Invest, Assets, Welfare, Coupon, Loan, Session
from yatang.modules import UserInfo

logger = logging.getLogger("app")
c = Cookies("./")
#投资秒标
class TenderWF:
    schedule = scheduler(time, sleep) 
    def __init__(self):
        pass

    def timming_exec(self, inc = 5):
        self.current_event = self.schedule.enter(inc, 0, self.welfare_tender, ( inc, ))
        self.tender_time = time()
        self.schedule.run()

    def asset_tender(self, inc):
        self.current_event = self.schedule.enter(inc, 0, self.asset_tender, ( inc, ))
        orginal_time = self.tender_time
        self.tender_time = time()  
        logger.debug('开始投资产标，间隔( ' + str(self.tender_time-orginal_time) + ' seconds )')
        cj = c.readCookie('richardxieq')        #c.dumpCookies(cj)

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
        assets = Assets(opener)
        assetList = []
        idx = 1
        while len(assetList) < 2:
            assetList.extend(assets.assetRequest(str(idx)))
            idx += 1
            if idx == 3:
                break

        print(assetList)

        for asset in assetList:
            print(asset)
            loan = Loan.loanRequest(opener, asset)
            invest.tender(loan, user_info)


    def welfare_tender(self, inc):
        self.current_event = self.schedule.enter(inc, 0, self.welfare_tender, ( inc, ))
        orginal_time = self.tender_time
        self.tender_time = time()  
        logger.debug('开始投秒标，间隔( ' + str(self.tender_time-orginal_time) + ' seconds )')
        session = Session()
        from conf import auto_tender_names
        for username in auto_tender_names:
            cj = c.readCookie(username)
            opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
            install_opener(opener)
            query = session.query(UserInfo).filter(UserInfo.name == username, UserInfo.website == 'yt')
            if query.count() == 0:
                continue
            user_info = query.one() 
            loaninfo = Welfare.walfareRequest(opener)  
            invest = Invest(user_info.name, opener)
            invest.tenderWF(loaninfo, user_info)      
        pass
    pass

if __name__ == '__main__':
   
    #初始化
    utils.initSys()
    conf.initConfig()
    Tender().timming_exec()