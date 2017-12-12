#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
from urllib.parse import urlencode
from yatang import Cookies, GrabTicketCash, GradRedPacket
from time import time, sleep
from datetime import datetime,timedelta
from sched import scheduler
from argparse import ArgumentParser
from tender import Tender
from tenderWF import TenderWF
from tenderCF import TenderCF
import sys,logging, yatang, json
from utils import initSys
from conf import initConfig, auto_tender_names

logger = logging.getLogger("app")

 #初始化
initSys()
initConfig()
schedule = scheduler(time, sleep)

c = Cookies('./')
cj = c.readCookie('richardxieq')
#c.dumpCookies(cj)
opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
install_opener(opener)

#定期检查是否有秒标，红包，现金券活动
def timming_exe(inc = 60): 
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动 
    schedule.enter(inc, 0, perform_command, (inc,)) 
    # 持续运行，直到计划时间队列变成空为止 
    schedule.run()
    pass
    
def perform_command(inc): 
    # 安排inc秒后再次运行自己，即周期运行 
    actIngressAddress()
    schedule.enter(inc, 0, perform_command, (inc,)) 
    pass
    
def actIngressAddress():
    values = {
        'fun': 'defaultShow'
    }
    postData = urlencode(values)
    headers = {
        'User-Agent': yatang.YT_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    req = Request(url = yatang.YTURLBASESSL + 'Account/actIngressAddress', data= postData.encode(encoding='UTF8'),  headers=headers, method='POST')
    jsonresp = None
    threads = []
    try:
        with opener.open(req, timeout=30) as response:
            if response.code == 200:
                jsonresp = json.loads(response.read().decode())
                if jsonresp['status'] == 200:
                    if 'welfare' in jsonresp['data'] and len(jsonresp['data']['welfare']['returnDatas']) > 0:
                        logger.info('秒标来了......')
                        for username in auto_tender_names:
                            t = TenderWF(username)
                            t.start()
                            threads.append(t)
                        pass
                    if 'gradRedPacketInfo' in jsonresp['data'] and len(jsonresp['data']['gradRedPacketInfo']['returnDatas']):
                        logger.info('红包来了......')
                        t = GradRedPacket(username)
                        t.start()
                        threads.append(t)
                        pass
                    if 'TicketCash' in jsonresp['data'] and len(jsonresp['data']['TicketCash']['returnDatas']):
                        logger.info('现金券来了 ......')
                        for username in auto_tender_names:
                            t = GrabTicketCash(username)
                            t.start()
                            threads.append(t)

    except URLError as e:
        logger.warn(e)
    except HTTPError as h:
        logger.warn(h)
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        logger.warn('Unexpected error:',  sys.exc_info()[0])

    for thread in threads:
        thread.join()
    return jsonresp

#python app.py -t crowdfunding  -v
if __name__ == '__main__':
    timming_exe()
    '''
    parser = ArgumentParser()
    parser.add_argument('-t', '--type')
    parser.add_argument('-amt', '--amount')
    parser.add_argument('-u', '--user')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        {
            'welfare' : TenderWF().timming_exec,
            'asset' : Tender(args.user if args.user is not None else 'richardxieq').timming_exec,
            'crowdfunding' : TenderCF(args.user if args.user is not None else 'richardxieq', 
                                        args.amount if args.amount is not None else 15000)
                                        .crowdfunding_tender,
            'test' : lambda : logger.info("未实现")
        }[args.type]()
    except AttributeError as attrerr:
        logger.info('无效的任务名：%s' % args.type)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        print("finally")
    '''
    