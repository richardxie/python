#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from urllib.request import HTTPCookieProcessor ,build_opener,install_opener,HTTPRedirectHandler
import logging,utils,conf
from yatang import Cookies, Account, Invest, Assets, Coupon, Loan, Session
from yatang.modules import UserInfo

logger = logging.getLogger("app")
c = Cookies("./")
class Tender:
    def __init__(self):
        pass

    def asset_tender(self):
        cj = c.readCookie('emmaye')
        #c.dumpCookies(cj)
        opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
        install_opener(opener)

        acc = Account(opener)
        accountinfo = acc.accountRequest()
        totalAmount = accountinfo.available

        session = Session()
        query = session.query(UserInfo).filter(UserInfo.name == "emmaye", UserInfo.website == 'yt')
        if query.count() == 0:
            return

        user_info = query.one()

        invest = Invest(user_info.name, opener)
        assets = Assets(opener)
        assetList = []
        idx = 1
        while len(assetList) < 3:
            assetList.extend(assets.assetRequest(str(idx)))
            idx += idx

        print(assetList)

        for asset in assetList:
            print(asset)
            loan = Loan.loanRequest(opener, asset)
            invest.tender(loan, user_info)


    def welfare_tender(self):
        pass
    pass

if __name__ == '__main__':
    #初始化
    utils.initSys()
    conf.initConfig()
    Tender().asset_tender()