#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from yatang import  Cookies, Signin, Invest, Account, Session
from yatang.Loan import Loan
from yatang.Welfare import Welfare
from sched import scheduler
from random import randint
from tzj import Signin as TZJSignin
from threading import Thread, active_count
from yatang.modules import UserInfo
import utils, time, logging, signal, os, base64
DEBUG = True
AUTO_TENDER = True
SIGNIN = True
TZJ_SIGNIN = True
YT_SIGNIN = True
reserved_amount = 5000

c = Cookies("./")
logger = logging.getLogger("app")

class signin_task(Thread):
    schedule = scheduler(time.time, time.sleep) 
    def __init__(self):
        Thread.__init__(self)
        self.is_exit = False
    
    def perform_command(self, inc):
        self.signin_command(inc)
        
    def timming_exe(self, inc = 20):
        self.current_event = self.schedule.enter(inc, 0, self.perform_command, ( inc,))
        self.signin_time = time.time()
        self.schedule.run()
        
    def run(self):
        self.is_exit = False
        self.timming_exe()

    def stop(self):
        self.is_exit = True
        if not self.schedule.empty():
            self.schedule.cancel(self.current_event)
    
    def is_stop(self):
        return self.is_exit

    def signin_command(self, inc):
        if self.is_exit: 
            return
        inc = randint(86400,93600)
        self.current_event = self.schedule.enter(inc, 0, self.perform_command, ( inc,))
        orginal_time = self.signin_time
        self.signin_time=time.time()  
        logger.info('start signin command after ' + str(self.signin_time-orginal_time) + ' seconds')
        
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
    schedule = scheduler(time.time, time.sleep) 
    def __init__(self):
        Thread.__init__(self)
        self.is_exit = False
        
    def perform_command(self, inc):
        self.tender_command(inc)
    
    def timming_exec(self, inc = 30):
        self.current_event = self.schedule.enter(inc, 0, self.perform_command, ( inc,))
        self.tender_time = time.time()
        self.schedule.run()
        
    def run(self):
        self.is_exit = False
        self.timming_exec()

    def stop(self):
        self.is_exit = True
        if not self.schedule.empty():
            self.schedule.cancel(self.current_event)
        pass

    def is_stop(self):
        return self.is_exit
        
    def tender_command(self, inc):
        if self.is_exit: 
            return
        self.current_event = self.schedule.enter(inc, 0, self.perform_command, ( inc,))
        orginal_time = self.tender_time
        self.tender_time=time.time()  
        logger.debug('start tender command after ' + str(self.tender_time-orginal_time) + ' seconds')
        from conf import auto_tender_names
        print auto_tender_names
        for username in auto_tender_names:
            cookie = c.readCookie(username)
            session = Session()
            query = session.query(UserInfo).filter(UserInfo.name == username)
            if query.count() == 0:
                continue
            user_info = query.one()
            trade_password = base64.b64decode(user_info.trade_password)
            print trade_password
            i = Invest(name = username, cookie=cookie)
            investList = i.investListRequest()
            for ivst in investList:
                ibid = ivst['id']
                        
                # filter loan with password
                if(ivst['borrowpwd']):
                    continue
                        
                if(int(ivst['borrow_type']) == 5):
                    loaninfo = Welfare.walfareRequest(i.opener)  
                    i.tenderWF(loaninfo, trade_password)      
                else:
                    loaninfo = Loan.loanRequest(i.opener, ibid)
                    i.tender(loaninfo, trade_password)
        pass

    pass

def handler(signum, frame):
    t1.stop()
    t2.stop()
    
    print "receive a signal %d, is_exit = %d"%(signum, True)

def main():
    #初始化
    utils.initSys()

    #signal handler
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    #签到
    if SIGNIN:
        t1.daemon = True
        t1.start()
    
    #自动投资
    if AUTO_TENDER:
        t2.daemon = True
        t2.run() #pyv8.so can't work in thread, run it in Main thread

if __name__ == '__main__':
    t1 = signin_task()
    t2 = tender_task()
    try:
        main()
        while 1:   
            alive=True  
            if t1.is_stop() and t2.is_stop():   
                alive=False  
            if not alive:   
                break  
    except KeyboardInterrupt, e: 
        print e
    
