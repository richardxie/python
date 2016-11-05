#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from threading import Thread
from sched import scheduler
from yatang import  Cookies, Signin, Invest, Account, Session
from yatang.Loan import Loan
from yatang.Welfare import Welfare
from yatang.modules import UserInfo
import yatang, tzj, utils, time, base64, logging
from Queue import Queue
from random import randint
from tzj import Signin as TZJSignin
from tzj import signin_names as tzj_signin_names

logger = logging.getLogger("app")
c = Cookies("./")
class signin_task(Thread):
    schedule = scheduler(time.time, time.sleep) 
    q = Queue()
    def __init__(self, mq):
        Thread.__init__(self)
        self.is_exit = False
        self.mainQueue = mq
    
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
        if tzj.SIGNIN:
            for name in tzj_signin_names:
                TZJSignin(name).signin()
        
        #雅堂签到
        if yatang.SIGNIN:
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
    q = Queue()
    def __init__(self, mq):
        Thread.__init__(self)
        self.is_exit = False
        self.mainQueue = mq
        
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
        for username in auto_tender_names:
            cookie = c.readCookie(username)
            session = Session()
            query = session.query(UserInfo).filter(UserInfo.name == username, UserInfo.website == 'yt')
            if query.count() == 0:
                continue
            user_info = query.one()
            trade_password = base64.b64decode(user_info.trade_password)
            i = Invest(name = username, cookie=cookie, task = self)
            investList = i.investListRequest()
            for ivst in investList:
                        
                # filter loan with password
                if(ivst['borrowpwd']):
                    continue
                if user_info.user_id == '000':
                    user_info.user_id = ivst['luserid']
                    session.commit()
                        
                if(int(ivst['borrow_type']) == 5):
                    loaninfo = Welfare.walfareRequest(i.opener)  
                    i.tenderWF(loaninfo, trade_password)      
                else:
                    loaninfo = Loan.loanRequest(i.opener, ivst)
                    i.tender(loaninfo, trade_password)
        pass

    pass
