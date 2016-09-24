#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from yatang import  Cookies, Signin, Invest, Account, Welfare
from yatang.Loan import Loan
from sched import scheduler
from random import randint
from tzj import Signin as TZJSignin
import utils, time, logging
DEBUG = True
AUTO_TENDER = False
SIGNIN = True
reserved_amount = 5000

c = Cookies("./")
schedule = scheduler(time.time, time.sleep) 
tender_schedule = scheduler(time.time, time.sleep)
logger = logging.getLogger("app")

def signin():
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动     
    schedule.enter(1, 0, signin_command, ( ))         
    #  # 持续运行，直到计划时间队列变成空为止         
    schedule.run()
    pass

def signin_command():
    inc = randint(86400,93600)
    schedule.enter(inc, 0, signin_command, ( ))
    global signin_time
    orginal_time = signin_time
    signin_time=time.time()  
    logger.info('start signin command after ' + str(signin_time-orginal_time) + ' seconds')
    
    #投之家签到
    TZJSignin("cmljaGFyZHhpZXE=", 'dHpqcm9vdEAyMDE2').signin()
    
    #雅堂签到
    cookies = c.readCookies()
    
    mail_list = []
    for cookie in cookies:
        data = Signin(cookie).signin()
        account = Account(cookie).accountRequest()
        if account is not None and data is not None:
            mail_list.append({'user':account, 'data': data})
    utils.EmailUtils().send(mail_list)
    
    pass

def auto_tender():
    # enter用来安排某事件的发生时间，从现在起第n秒开始启动     
    tender_schedule.enter(1, 0, tender_command, ( ))         
    #  # 持续运行，直到计划时间队列变成空为止         
    tender_schedule.run()
    pass
   

def tender_command():
    tender_schedule.enter(60, 0, tender_command, ( ))
    global tender_time
    orginal_time = tender_time
    tender_time=time.time()  
    logger.debug('start tender command after ' + str(tender_time-orginal_time) + ' seconds')
    cookie = c.readCookie("richardxieq")
    i = Invest(cookie)
    investList = i.investListRequest()
    for ivst in investList:
        ibid = ivst['id']
                
        # filter loan with password
        if(ivst['borrowpwd']):
            continue
                
        if(int(ivst['borrow_type']) == 5):
            loaninfo = Welfare.Welfare.walfareRequest(i.opener)  
            i.tenderWF(loaninfo)      
        else:
            loaninfo = Loan.loanRequest(i.opener, ibid)
            i.tender(loaninfo)
    pass

def main():
    #初始化
    utils.initSys()
    
    #签到
    if SIGNIN:
        signin()
    
    #自动投资
    if AUTO_TENDER:
        auto_tender()

if __name__ == '__main__':
    signin_time=time.time()
    tender_time=time.time()
    main()