#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from urllib2 import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler
from urllib import urlencode
import yatang, json

class Coupon: 
    def __init__(self, cookie, borrowNum):
        self.cookie = cookie
        self.borrowNum = borrowNum
        if cookie is not None:
            self.opener = build_opener(HTTPCookieProcessor(self.cookie), HTTPRedirectHandler())
            install_opener(self.opener)

    def __repr__(self):
        return "<Coupon(borrowNum='%s')>" % (
                self.borrowNum)

    def couponListRequest(self):
        values = {
            'investMoney':'',
            'borrowNum': self.borrowNum,
            'pageNum':1
        }
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASE + 'Ajax/getUserCoupon', data.encode(encoding='UTF8'), headers)
        jsonresp = None;
        try:
            response = self.opener.open(req, timeout=30)
            if response.code == 200:
                jsonresp = json.loads(response.read().decode())
        except URLError, e:
            loadsgging.getLogger("app").warn(e)
        except HTTPError as h:
            logging.getLogger("app").warn(h)

         return jsonresp
