#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
#抢现金券
from datetime import datetime,timedelta
import os, sys, json
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

from utils import httpRequest, money
import yatang, logging, traceback

logger = logging.getLogger('app')

"""
https://jr.yatang.cn/GrabTicketCash/getActivityInfo

{
    "status":1,
    "data":{
        "activityName":"\u6d4b\u8bd5\u9650\u989d\u62a2\u73b0\u91d1\u5238",
        "activityTotalMoney":60000,
        "rateOfProgress":0,
        "activityConfineMoney":200,
        "activityStartTime":1512471600,
        "activityEndTime":1512472800,
        "activityNowTime":1512437014,
        "time":34586,
        "activityStartMoney":500,
        "activityRate":13.88,
        "useMoney":6025,
        "useInvestMaxMoney":6025,
        "userAlreadyMoney":200,
        "key":"fd7b4efee67f74a02441f10017403695",
        "activityCode":"OA",
        "activityInfo":""
        },
    "info":"success
    """
class TicketCash: 
    def __init__(self,activityName=None, activityTotalMoney=None, activityConfineMoney=None, activityStartTime=None, time = None, activityStartMoney = None,  key = None, activityCode = None):
        self.activityName = activityName
        self.activityTotalMoney = activityTotalMoney
        self.activityConfineMoney = activityConfineMoney
        self.activityStartTime = activityStartTime
        self.time = time
        self.activityStartMoney = activityStartMoney
        self.key = key
        self.activityCode = activityCode
          
    def __repr__(self):
        return "<现金券(项目名称='%s',项目金额='%.2f', 起投金额='%.2f',可投金额='%.2f',编号='%s', 键值='%s')>" % (
               self.activityName, self.activityTotalMoney, self.activityStartMoney, self.useMoney, self.activityCode, self.key)
    
    @staticmethod
    def ticketCash_detail(jsonObj):
        logger.debug("现金券详细信息解析")
        ticketCash = TicketCash()
        d = dict((key,value) for key, value in jsonObj.items() if key in ticketCash.__dict__) 
        ticketCash.__dict__ = d
        logger.debug(str(ticketCash))
        return ticketCash


class GrabTicketCash: 
    def __init__(self, opener):
        self.opener = opener
    
    def ticketCashDetailRequest(self):
        resp = httpRequest(self.opener,  yatang.YTURLBASESSL + "/GrabTicketCash/getActivityInfo")
        jsonresp = {}
        if resp and resp.code == 200:
            jsonresp = json.loads(resp.read().decode('UTF-8'))
            if jsonresp and 'status' in jsonresp:
                if int(jsonresp['status']) == 1:
                    return TicketCash.ticketCash_detail(jsonresp['data'])


    
if __name__ == '__main__':
    from Cookies import Cookies
    from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
    c = Cookies()
    cj = c.readCookie('emmaye')
    #c.dumpCookies(cj)
    opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
    install_opener(opener)

    grabTicketCash = GrabTicketCash(opener)
    grabTicketCash.ticketCashDetailRequest()