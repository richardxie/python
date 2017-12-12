#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
#抢现金券
from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
from urllib.parse import urlencode
from datetime import datetime,timedelta
from time import time, sleep
from threading import Thread, current_thread

import os, sys, json, base64
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

from utils import httpRequest, money, Encryptor
import logging, traceback
from yatang import Cookies, GrabTicketCash
from yatang.modules import UserInfo
import yatang,utils,conf

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
    def __init__(self,
                    activityName = None,        #名称
                    activityTotalMoney = None,  #现金券总额
                    activityConfineMoney=None,  #限抢额
                    useMoney = None,            #可用金额
                    useInvestMaxMoney = None,   #最大可投金额
                    activityStartTime=None,     #开始时间
                    activityEndTime = None,     #结束时间
                    time = None,                #等待时间（现在时间 - 开始时间）
                    activityStartMoney = None,  #起投金额
                    activityRate = None,        #年回报率
                    key = None,                 #加密盐值
                    activityCode = None         #编号
                    ):
        self.activityName = activityName
        self.activityTotalMoney = activityTotalMoney
        self.activityConfineMoney = activityConfineMoney
        self.useMoney = useMoney
        self.useInvestMaxMoney = useInvestMaxMoney
        self.activityStartTime = activityStartTime
        self.activityEndTime = activityEndTime
        self.time = time
        self.activityStartMoney = activityStartMoney
        self.activityRate = activityRate
        self.key = key
        self.activityCode = activityCode
          
    def __repr__(self):
        return "<现金券(项目名称='%s',项目金额='%.2f', 起投金额='%.2f',可投金额='%.2f',编号='%s', 键值='%s')>" % (
               self.activityName, self.activityTotalMoney, self.activityStartMoney, self.useInvestMaxMoney, self.activityCode, self.key)
    
    @staticmethod
    def ticketCash_detail(jsonObj):
        logger.debug("现金券详细信息解析")
        ticketCash = TicketCash()
        d = dict((key,value) for key, value in jsonObj.items() if key in ticketCash.__dict__) 
        ticketCash.__dict__ = d
        logger.debug(ticketCash)
        return ticketCash


class GrabTicketCash(Thread): 
    def __init__(self, username):
        Thread.__init__(self)
        self.username = username
        self.encryptor = Encryptor()
    
    def run(self):
        c = Cookies()
        cj = c.readCookie(self.username)
        #c.dumpCookies(cj)
        self.opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
        install_opener(self.opener)

        session = yatang.Session()
        query = session.query(UserInfo).filter(UserInfo.name == username, UserInfo.website == 'yt')
        if query.count() != 0:
            self.user_info = query.one()
        else:
            logger.warn('用户不存在：%s' % (self.username))
            return

        for i in range(2):
            res = self.ticketCashDetailRequest()
            if res == None:
                break

            delta = res.time
            startTime = datetime.fromtimestamp(res.activityStartTime)
            print(startTime.strftime("%Y-%m-%d %H:%M:%S"))
            now = datetime.now()
            delta2 = (startTime - now).seconds

            print("time delta: %d"%(delta2 - delta))

            if delta2 < 0 :
                logger.warn(' 开始时间已过， 直接执行！%d' % delta2)
                res = self.grabTicketCash(res)
                break
            elif delta2 > 600:
                logger.info('%s 先等待%d秒后开始执行抢现金券任务！ ' % (self.user_info.name, delta2 - 600))
                sleep(delta2 - 600)
            else:
                logger.info('%s %d秒后开始执行抢现金券任务！ ' % (self.user_info.name, delta))
                sleep(delta2)
                res = self.grabTicketCash(res)
                break

            logger.debug(res)
            pass

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
            'money': ticketCash.useInvestMaxMoney,
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
                    logger.debug("提交抢现金券请求结果：%s", jsonresp)
                    if jsonresp and 'status' in jsonresp:
                        if int(jsonresp['status']) == 1:
                            sleep(1) #稍等一下在查询结果
                            self.pollingResult(ticketCash.activityCode, jsonresp['data'])
        except URLError as e:
            logger.warn(e)
        except HTTPError as h:
            logger.warn(h)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logger.warn('Unexpected error:',  sys.exc_info()[0])

        return jsonresp

    def pollingResult(self, code, jsonObj):
        logger.debug("查询提交结果")
        values = {
            'gradnum': jsonObj['gradNum'],
            'id': code
        }
        postData = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
        req = Request(url = yatang.YTURLBASESSL + 'GrabTicketCash/checkTicketCashQueen', data= postData.encode(encoding='UTF8'),  headers=headers, method='POST')
        jsonresp = None
        try:
            with self.opener.open(req, timeout=30) as response:
                if response.code == 200:
                    jsonresp = json.loads(response.read().decode())
                    if jsonresp and 'status' in jsonresp:
                        if int(jsonresp['status']) == 1:
                            logger.debug('查询抢现金券状态成功')
        except URLError as e:
            logger.warn(e)
        except HTTPError as h:
            logger.warn(h)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logger.warn('Unexpected error:',  sys.exc_info()[0])
        logger.debug("查询提交结果: %s", jsonresp)
        return jsonresp
    
if __name__ == '__main__':
    '''
    from Cookies import Cookies
    from yatang import Session
    from yatang.modules import UserInfo
    from urllib.parse import urlencode
    from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
   '''
    #初始化
    utils.initSys()
    conf.initConfig()
    from conf import auto_tender_names
    threads = []
    for username in auto_tender_names:
        t = GrabTicketCash(username)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()
   
    logger.info('抢现金券任务 %s 完成.' % current_thread().name)