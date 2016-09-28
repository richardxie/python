#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from yatang import  Cookies, Signin, Invest, Account
from yatang.Loan import Loan
from yatang.Welfare import Welfare
from sched import scheduler
from random import randint
from tzj import Signin as TZJSignin
from threading import Thread, active_count
import utils, time, logging, signal, os
DEBUG = True
AUTO_TENDER = True
SIGNIN = True
TZJ_SIGNIN = True
YT_SIGNIN = True
reserved_amount = 5000

c = Cookies("./")
schedule = scheduler(time.time, time.sleep) 
tender_schedule = scheduler(time.time, time.sleep)
logger = logging.getLogger("app")

class signin_task(Thread):
    def __init__(self):
        Thread.__init__(self)
    
    def perform_command(self, inc):
        self.signin_command(inc)
        
    def timming_exe(self, inc = 20):
        global current_event
        current_event = schedule.enter(inc, 0, self.perform_command, ( inc,))
        schedule.run()
        
    def run(self):
        self.timming_exe()
        
    def signin_command(self, inc):
        global is_exit
        if is_exit: 
            return
        inc = randint(86400,93600)
        global current_event
        current_event = schedule.enter(inc, 0, self.perform_command, ( inc,))
        global signin_time
        orginal_time = signin_time
        signin_time=time.time()  
        logger.info('start signin command after ' + str(signin_time-orginal_time) + ' seconds')
        
        #投之家签到
        if TZJ_SIGNIN:
            TZJSignin("cmljaGFyZHhpZXE=", 'dHpqcm9vdEAyMDE2').signin()
        
        #雅堂签到
        if YT_SIGNIN:
            cookies = c.readCookies()
            
            mail_list = []
            for cookie in cookies:
                account = Account(cookie).accountRequest()
                data = Signin(cookie =cookie,
                            name = account.name).signin()
                if account is not None and data is not None:
                    mail_list.append({'user':account, 'data': data})
            utils.EmailUtils().send(mail_list)
        
        pass

class tender_task(Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def perform_command(self, inc):
        self.tender_command(inc)
    
    def timming_exec(self, inc = 30):
        global tender_current_event
        tender_current_event = tender_schedule.enter(inc, 0, self.perform_command, ( inc,))
        tender_schedule.run()
        
    def run(self):
        self.timming_exec()
        
    def tender_command(self, inc):
        global is_exit
        if is_exit: 
            return
        global tender_current_event
        tender_current_event = tender_schedule.enter(inc, 0, self.perform_command, ( inc,))
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
                loaninfo = Welfare.walfareRequest(i.opener)  
                i.tenderWF(loaninfo)      
            else:
                loaninfo = Loan.loanRequest(i.opener, ibid)
                i.tender(loaninfo)
        pass

    pass

def handler(signum, frame):
    print current_event
    print tender_current_event
    global is_exit
    is_exit = True

    if not schedule.empty():
        schedule.cancel(current_event)
    if not tender_schedule.empty():
        tender_schedule.cancel(tender_current_event)
    
    print "receive a signal %d, is_exit = %d"%(signum, is_exit)

def main():
    #初始化
    utils.initSys()

    #signal handler
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    #签到
    if SIGNIN:
        t1 = signin_task()
        t1.daemon = True
        t1.start()
    
    #自动投资
    if AUTO_TENDER:
        t2 = tender_task()
        t2.daemon = True
        t2.start()

if __name__ == '__main__':
    signin_time=time.time()
    current_event = None
    tender_time=time.time()
    tender_current_event = None
    is_exit = False
    main()
    while active_count() > 1:  #1 means  current main thread 
        time.sleep(1)
