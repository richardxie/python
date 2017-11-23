#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
from urllib.parse import urlencode
import json, logging, os, sys
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

import yatang, logging, traceback
from utils import httpRequest, money
from time import time, sleep
from threading import Thread, current_thread

logger = logging.getLogger('app')

#抢红包
class RedEnvelope: 
    def __init__(self, projectId, usableMoney, redPacketVal, redPacketUseVal,leftTime):
        self.opener = opener
        self.projectId = projectId
        self.usableMoney = usableMoney
        self.redPacketVal = redPacketVal
        self.redPacketUseVal = redPacketUseVal
        self.leftTime = leftTime

    def __repr__(self):
        return "<Redpacket(项目编号='%s')>" % (
                self.projectId)

    @staticmethod
    def redEnvelope_info(html):
        logger.debug("抢红包信息解析中...")
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        try:
            projectID_element = dom.xpath("//*[@id='projectId']")
            if projectID_element and len(projectID_element) > 0:
                projectID = projectID_element[0].attrib['value']
            usableMoney_element = dom.xpath("//*[@id='usableMoney']")
            if usableMoney_element and len(usableMoney_element) > 0:
                usableMoney = money(usableMoney_element[0].text)
            redPacketVal_element = dom.xpath("//*[@id='redPacketVal']")
            if redPacketVal_element and len(redPacketVal_element) > 0:
                redPacketVal = int(redPacketVal_element[0].attrib['value'])
            redPacketUseVal_element = dom.xpath("//*[@id='redPacketUseVal']")
            if redPacketUseVal_element and len(redPacketUseVal_element) > 0:
                redPacketUseVal = money(redPacketUseVal_element[0].attrib['value'])
            
            leftTime_element = dom.xpath("//*[@id='leftTime']")
            if leftTime_element and len(leftTime_element) > 0:
                leftTime = int(leftTime_element[0].attrib['value'])
            
            return RedEnvelope(
                projectId = projectID,
                usableMoney = usableMoney,
                redPacketVal = redPacketVal,
                redPacketUseVal = redPacketUseVal,
                leftTime = leftTime
            )
        except Exception as e:
            print (e)
            traceback.print_exc() 
            logger.warn("oops, 抢红包页面解析失败!")

class GradRedPacket(Thread):
    def __init__(self, opener, vcode):
        Thread.__init__(self)
        self.opener = opener
        self.vcode = vcode

    def run(self):
        re = self.gradRedPacketRequest()
        delta = re.leftTime
        sleep( delta )
        res = c.gradStart(re)
        logging.getLogger("app").log(res)
        pass

    def gradRedPacketRequest(self):
        resp = httpRequest(opener, yatang.YTURLBASESSL + "/GradRedPacket")
        if resp and resp.code == 200:
            return RedEnvelope.redEnvelope_info(resp)
    
    def gradStart(self, redEnvelope):
        values = {
            'money': int(redEnvelope.usableMoney / redEnvelope.redPacketUseVal) * redEnvelope.redPacketUseVal,
            'projectId': redEnvelope.projectId,
            'vcode': self.vcode
        }
        postData = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
        req = Request(url = yatang.YTURLBASESSL + 'GradRedPacket/gradStart', data= postData.encode(encoding='UTF8'),  headers=headers, method='POST')
        jsonresp = None
        try:
            with self.opener.open(req, timeout=30) as response:
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
    from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
    from Cookies import Cookies
    
   
    auto_tender_names = [
        {'username':'emmaye',  'vcode':'123'},
        {'username':'richardxieq', 'vcode':'123'}
        ]
    threads = []
    for user in auto_tender_names:
        c = Cookies()
        cj = c.readCookie(user['username'])
        #c.dumpCookies(cj)
        opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
        install_opener(opener)
        t = GradRedPacket(opener, user['vcode'])
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()
    
    logger.info('抢红包任务 %s 完成.' % current_thread().name)
    
    pass