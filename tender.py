#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from threading import Thread
from sched import scheduler
from yatang import  Cookies, Signin, Invest, Account, Session
from yatang.Loan import Loan
from yatang.Welfare import Welfare
from yatang.modules import UserInfo, FinancingInfo
from yatang.Financing import Financing
import yatang, tzj, utils, time, base64, logging
from Queue import Queue
from random import randint
from tzj import Signin as TZJSignin
from tzj import signin_names as tzj_signin_names

logger = logging.getLogger("app")
c = Cookies("./")

class tender:  
    def tender_command(self):
        logger.debug('start tender command')
        from conf import auto_tender_names
        for username in auto_tender_names:
            cookie = c.readCookie(username)
            session = Session()
            query = session.query(UserInfo).filter(UserInfo.name == username, UserInfo.website == 'yt')
            if query.count() == 0:
                continue
            user_info = query.one()
            loaninfo = Welfare.walfareRequest(i.opener)  
            i.tenderWF(loaninfo, user_info)   
        pass

    pass

if __name__ == '__main__':
    #初始化
    utils.initSys()
    tender().tender_command()

