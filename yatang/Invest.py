#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from urllib2 import Request, install_opener,build_opener,HTTPCookieProcessor, HTTPRedirectHandler
from urllib import urlencode
from math import floor
import yatang, json, logging, math
from modules import InvestInfo, WelfareInfo
from utils import encryptTradePassword

logger = logging.getLogger("app")

class Invest: 

    def __init__(self, name, cookie, task):
        self.cookie = cookie
        self.name = name
        self.task = task;
        if cookie is not None:
            self.opener = build_opener(HTTPCookieProcessor(self.cookie), HTTPRedirectHandler())
            install_opener(self.opener)
              
    def tender(self, loan, tradepwd="root@2014"):
        logger.info(self.name + " is tendering a Loan.")
        import app
        ammount = int(floor(loan.available_cash)) - app.reserved_amount
        if(ammount > loan.minAmount):
                salt = loan.uniqKey
                ppay = encryptTradePassword(tradepwd, salt, self.task)
                # coupon info
                lunchid = "0"
                
                couponinfo = yatang.Coupon(self.cookie, loan.borrowNum).couponListRequest()
                if('data' in couponinfo and len(couponinfo['data'])):
                    lunchid = couponinfo['data'][0]['id']
                    ammount = couponinfo['data'][0]['user_constraint']
                else:
                    logger.info("没有合适的红包")
                    return
                # buy
                values = {
                    '__hash__': loan.__hash__,
                    'ibnum': loan.borrowNum,
                    'lunchId': lunchid,  # 红包ID
                    'amount': ammount,
                    'p_pay': ppay,
                    'user_id': '54808'
                    }
                buyinfo = self.buyRequest(values)
                if('tnum' in buyinfo):
                    self.tender_info(loan.borrowNum, buyinfo['tnum'])
                    import uuid
                    invest = InvestInfo(id=str(uuid.uuid1()),                             
                        name=loan.uid,
                        amount = 100)
                    session = yatang.Session()
                    session.add(invest)
                    session.commit()
                
        pass 
    
    def tenderWF(self, welfare, tradepwd= "root@2014"):
        if welfare == None:
            logging.warn("welfare is none!")
            return
        logging.debug(self.name +" want to tender a Welfare:" + str(welfare.available_cash) + ":" + str(welfare.can_tender))

        if(welfare.available_cash > welfare.zxtbe and welfare.can_tender):
            logging.info(self.name +" is tendering a Welfare:" + str(welfare.available_cash)+ ":" + welfare.uniqKey)
            salt = welfare.uniqKey
            ppay = encryptTradePassword(tradepwd, salt, self.task)
            # buy 秒标
            values = {
                '__hash__': welfare.hash_value,
                'ibnum': welfare.borrowNum,
                'lunchId': '0',  # 红包ID
                'amount': int(math.floor(welfare.available_cash)),
                'p_pay': ppay,
                'user_id': '54808'
            }
            buyinfo = self.buyRequest(values)
            if('tnum' in buyinfo):
                session = yatang.Session()
                query = session.query(WelfareInfo).filter(WelfareInfo.ibid == welfare.ibid)
                if query.count() == 0:
                    welfare_info = WelfareInfo.fromWelfare(welfare)
                    session.add(welfare_info)
                    session.commit()
                self.tender_info(welfare.borrowNum, buyinfo['tnum'])
        pass     
    
    def buyRequest(self, values):
        logging.info('tender start:' + str(values['amount']))
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASESSL + 'Invest/checkppay', data.encode(encoding='UTF8'), headers)
        response = self.opener.open(req)
        if response.code == 200 :
            resp_data =response.read().decode()
            try:
                jsonresp = json.loads(resp_data)
            except ValueError:
                logger.warn("data was not valid JSON")
                logger.warn(resp_data)
                jsonresp = {}
        return jsonresp

    def tender_info(self, borrow_num, tnum):
        values = {
            'borrow_num':borrow_num,
            'tnum': tnum
        }
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASE + 'Public/tenderinfo', data.encode(encoding='UTF8'), headers)
        response = self.opener.open(req)
        if response.code == 200 :
            resp_data =response.read().decode()
            try:
                jsonresp = json.loads(resp_data)
            except ValueError:
                logger.warn("data was not valid JSON")
                logger.warn(resp_data)
                jsonresp = {}
            return jsonresp
    
    def investListRequest(self, typeList=[5]):
        values = {
            'mode':1,
            'tpage[page]':1,
            'tpage[size]':20
        }
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASE + 'index.php?s=/Invest/GetBorrowlist', data.encode(encoding='UTF8'), headers)
        response = self.opener.open(req)
        if response.code == 200:
            resp_data = response.read().decode()
            try:
                jsonresp = json.loads(resp_data)
            except ValueError:
                logger.warn("data was not valid JSON")
                logger.warn(resp_data)
                return [];
        

            if(len(typeList)):
                aList = []
                for loan in jsonresp['data']['Rows']:
                    bt = int(loan['borrow_type'])
                    if bt in typeList: #and int(loan["time_limit"]) == 3:
                        if bt in [1, 9] and int(loan["time_limit"]) == 3:
                            aList.append(loan)
                        else:
                            aList.append(loan)
                return aList
            else:
                return jsonresp['data']['Rows']
        else:
            return []
