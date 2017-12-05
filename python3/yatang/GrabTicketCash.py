#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
#抢现金券
from datetime import datetime,timedelta
import os, sys, json, base64
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

from utils import httpRequest, money, Encryptor
import yatang, logging, traceback
import logging,utils,conf
from time import time, sleep
from threading import Thread, current_thread

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
    def __init__(self,activityName=None, activityTotalMoney=None, activityConfineMoney=None, 
                    useMoney = None,activityStartTime=None, time = None, activityStartMoney = None, 
                    activityRate = None, key = None, activityCode = None):
        self.activityName = activityName
        self.activityTotalMoney = activityTotalMoney
        self.activityConfineMoney = activityConfineMoney
        self.useMoney = useMoney
        self.activityStartTime = activityStartTime
        self.time = time
        self.activityStartMoney = activityStartMoney
        self.activityRate = activityRate
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
        logger.debug(ticketCash)
        return ticketCash


class GrabTicketCash(Thread): 
    def __init__(self, opener, user_info):
        Thread.__init__(self)
        self.opener = opener
        self.user_info = user_info
        self.encryptor = Encryptor()
    
    def run(self):
        for i in range(2):
            res = self.ticketCashDetailRequest()
            if res == None:
                break

            delta = res.time

            if delta < 0 :
                logger.warn(' 开始时间已过， 直接执行！%d' % delta)
                res = self.grabTicketCash(res)
                break
            elif delta > 600:
                logger.info('%s 先等待%d秒后开始执行抢现金券任务！ ' % (self.user_info.name, delta - 600))
                sleep(delta - 600)
            else:
                logger.info('%s %d秒后开始执行抢现金券任务！ ' % (self.user_info.name, delta))
                sleep(delta)
                res = self.grabTicketCash(res)
                break

            logger.log(res)

    def ticketCashDetailRequest(self):
        resp = httpRequest(self.opener,  yatang.YTURLBASESSL + "/GrabTicketCash/getActivityInfo")
        jsonresp = {}
        if resp and resp.code == 200:
            jsonresp = json.loads(resp.read().decode('UTF-8'))
            if jsonresp and 'status' in jsonresp:
                if int(jsonresp['status']) == 1:
                    return TicketCash.ticketCash_detail(jsonresp['data'])

    def grabTicketCash(self, ticketCash):
        salt = ticketCash.key
        ppay = self.encryptor.encryptPassword(base64.b64decode(self.user_info.trade_password).decode('utf-8'), salt)

        values = {
            'id': ticketCash.activityCode,
            'money': ticketCash.useMoney,
            'pwd': ppay
        }
        postData = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
        req = Request(url = yatang.YTURLBASESSL + 'GrabTicketCash/grabTicketCash', data= postData.encode(encoding='UTF8'),  headers=headers, method='POST')
        jsonresp = None
        try:
            with self.opener.open(req, timeout=30) as response:
                if response.code == 200:
                    jsonresp = json.loads(response.read().decode())
                    if jsonresp and 'status' in jsonresp:
                        if int(jsonresp['status']) == 1:
                            logger.debug(jsonresp)
                            self.pollingResult(jsonresp)
        except URLError as e:
            logger.warn(e)
        except HTTPError as h:
            logger.warn(h)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logger.warn('Unexpected error:',  sys.exc_info()[0])

        return jsonresp

    def pollingResult(self, jsonObj):
        logger.debug("查询提交结果")
        pass
    
if __name__ == '__main__':
    from Cookies import Cookies
    from yatang import Session
    from yatang.modules import UserInfo
    from urllib.parse import urlencode
    from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
    #初始化
    utils.initSys()
    conf.initConfig()
    from conf import auto_tender_names
    threads = []
    for username in auto_tender_names:
        c = Cookies()
        cj = c.readCookie(username)
        #c.dumpCookies(cj)
        opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
        install_opener(opener)

        session = Session()
        query = session.query(UserInfo).filter(UserInfo.name == username, UserInfo.website == 'yt')
        if query.count() != 0:
            user_info = query.one()
            t = GrabTicketCash(opener, user_info)
            t.start()
            threads.append(t)

    for thread in threads:
        thread.join()
   
    logger.info('抢现金券任务 %s 完成.' % current_thread().name)