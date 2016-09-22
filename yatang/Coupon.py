#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from urllib2 import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler
from urllib import urlencode
import yatang, json

class Coupon: 
    def __init__(self, cookie, borrowNum):
        self.cookie = cookie
        self.borrowNum = borrowNum
        self.opener = build_opener(HTTPCookieProcessor(self.cookie), HTTPRedirectHandler())
        install_opener(self.opener)

    @staticmethod
    def couponListRequest(opener, borrowNum):
        values = {
            'investMoney':'',
            'borrowNum': borrowNum,
            'pageNum':1
        }
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASE + 'Ajax/getUserCoupon', data.encode(encoding='UTF8'), headers)
        response = opener.open(req)
    
        jsonresp = json.loads(response.read().decode())
        print(jsonresp)
        return jsonresp