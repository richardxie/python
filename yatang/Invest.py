#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from PyV8 import JSContext
from urllib2 import Request, install_opener,build_opener,HTTPCookieProcessor, HTTPRedirectHandler
from urllib import urlencode
from math import floor
import yatang, json

class Invest: 

    def __init__(self, cookie):
        self.cookie = cookie
        self.opener = build_opener(HTTPCookieProcessor(self.cookie), HTTPRedirectHandler())
        install_opener(self.opener)
              
    def tender(self, loan, tradepwd="root@2014"):
        print "i'm tendering a Loan."
        ammount = int(floor(loan.available_cash))
        import app
        if(ammount > loan.minAmount and ammount > app.reserved_amount):
                salt = loan.uniqKey
                ppay = self.encryptTradePassword(tradepwd, salt)
                # coupon info
                lunchid = "0"
                
                couponinfo = yatang.Coupon.couponListRequest(self.opener, loan.borrowNum)
                if('data' in couponinfo and len(couponinfo['data'])):
                    lunchid = couponinfo['data'][0]['id']
                    ammount = couponinfo['data'][0]['user_constraint']
                # buy
                values = {
                    '__hash__': loan.__hash__,
                    'ibnum': loan.borrowNum,
                    'lunchId': lunchid,  # 红包ID
                    'amount': ammount,
                    'p_pay': ppay,
                    'user_id': '54808'
                    }
                buyinfo = self.buyRequest(values)
                if('tnum' in buyinfo):
                    self.tender_info(loan.borrowNum, buyinfo['tnum'])
                
        pass 
    
    def tenderWF(self, Welfare, tradepwd= "root@2014"):
        print "i'm tendering a Welfare."
        encryptedPwd = self.encryptTradePassword(tradepwd, "hao123")
        print encryptedPwd
        pass     
    
    def buyRequest(self, values):
        print 'buy start.'
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASE + 'Invest/checkppay', data.encode(encoding='UTF8'), headers)
        response = self.opener.open(req)
        jsonresp = json.loads(response.read().decode())
        print jsonresp
        return jsonresp

    def tender_info(self, borrow_num, tnum):
        values = {
            'borrow_num':borrow_num,
            'tnum': tnum
        }
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASE + 'Public/tenderinfo', data.encode(encoding='UTF8'), headers)
        response = self.opener.open(req)
    
        jsonresp = json.loads(response.read().decode())
        print jsonresp
        return jsonresp

    def encryptTradePassword(self, tradepassword, uniqkey):
        with JSContext() as jsctx:
            with open("encrypt.js") as jsfile:
                jsctx.eval(jsfile.read())
                encryptFunc = jsctx.locals.encrypt2;
                pwd = encryptFunc(tradepassword, uniqkey)
        return pwd
    
    def investListRequest(self, typeList=(1,5,9)):
        values = {
            'mode':1,
            'tpage[page]':1,
            'tpage[size]':20
        }
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASE + 'index.php?s=/Invest/GetBorrowlist', data.encode(encoding='UTF8'), headers)
        response = self.opener.open(req)
    
        jsonresp = json.loads(response.read().decode())
        if(len(typeList)):
            aList = []
            for loan in jsonresp['data']['Rows']:
                if int(loan['borrow_type']) in typeList:
                    aList.append(loan)
            return aList
        else:
            return jsonresp['data']['Rows']
