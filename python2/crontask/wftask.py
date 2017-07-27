#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from yatang import  Cookies, Signin, Invest, Account, Session
from yatang.Loan import Loan
from yatang.Welfare import Welfare
from yatang.modules import UserInfo, FinancingInfo
from yatang.Financing import Financing
import yatang, tzj, utils, time, base64, logging

logger = logging.getLogger("app")
c = Cookies("./")
class tender_task:
	Welfare loaninfo;
    def tender_command(self, Welfare wf):
		self.loaninfo = wf
        logger.debug(' start cron tender command ')
		
        from conf import auto_tender_names
        for username in auto_tender_names:
            cookie = c.readCookie(username)
            session = Session()
            query = session.query(UserInfo).filter(UserInfo.name == username, UserInfo.website == 'yt')
            if query.count() == 0:
                continue
            user_info = query.one()
            i = Invest(name = username, cookie=cookie, task = None);
			i.tenderWF(loaninfo, user_info)  
        pass

    pass
	
if __name__ == '__main__':
    print 'cron job: cron 秒标'
    #初始化
    utils.initSys()
    tender_task().tender_command()
