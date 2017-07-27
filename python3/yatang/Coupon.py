#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
from urllib.parse import urlencode
import json, logging, os, sys
pythonpath ='E:/SlProject/v2'
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

import yatang
from Cookies import Cookies

class Coupon: 
    def __init__(self, cookie, borrowNum="1216Z8ULU0000665"):
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
            'investMoney': '',
            'borrowNum': '12196M4GM0000848',
            'pageNum': '1'
        }
        data = urlencode(values).encode('utf-8')
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://jr.yatang.cn/Invest/ViewBorrow/ibid/1084520'
        }
        req = Request(yatang.YTURLBASE + 'Ajax/getUserCoupon', data,  headers)
        jsonresp = None
        try:
            response = self.opener.open(req, timeout=300)
            if response.code == 200:
                jsonresp = json.loads(response.read().decode())
        except URLError as e:
            logging.getLogger("app").warn(e)
        except HTTPError as h:
            logging.getLogger("app").warn(h)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logging.getLogger("app").warn('Unexpected error:',  sys.exc_info()[0])

        return jsonresp

if __name__ == '__main__':
    c = Cookies()
    cj = c.readCookie('richardxieq')
    c.dumpCookies(cj)

    c = Coupon(cj)
    c.couponListRequest()
    pass