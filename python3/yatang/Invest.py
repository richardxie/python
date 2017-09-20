#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

from urllib.request import Request, install_opener,build_opener,HTTPCookieProcessor, HTTPRedirectHandler, URLError, HTTPError
from urllib.parse import urlencode
from math import floor

import json, logging, os, sys, math, base64, socket
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

import yatang
from modules import InvestInfo, WelfareInfo
from Coupon import Coupon
from Redpacket import Redpacket
from Assets import Asset, Assets
from utils import Encryptor

logger = logging.getLogger("app")

class Invest: 
    def __init__(self, name, opener, amount = None):
        self.encryptor = Encryptor()
        self.name = name #用户名
        self.opener = opener
        self.amount = amount #投资金额

    #根据红包来确定投资金额      
    def tender(self, loan, user_info):
        logger.info(self.name + " 开始投资资产标.")
        ammount = int(floor(loan.available_cash)) - yatang.reserved_amount
        if(ammount > loan.minAmount):
                salt = loan.uniqKey
                ppay = self.encryptor.encryptTradePassword(base64.b64decode(user_info.trade_password).decode('utf-8'), salt)
                # coupon info
                lunchid = "0"
                
                couponinfo = Coupon(self.opener, loan.borrowNum).couponListRequest()
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
                    'user_id': user_info.user_id
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
    
    #用户的可投金额来投资
    def tenderWF(self, welfare, user_info):
        if welfare == None:
            logger.warn("无效的开心利是信息")
            return
        logger.debug(self.name +" 准备投开心利是:" + str(welfare.available_cash) + ":" + str(welfare.can_tender))

        if(welfare.available_cash > welfare.zxtbe and welfare.can_tender):
            logger.info(self.name +" 开始投开心利是:" + str(welfare.available_cash)+ ":" + welfare.uniqKey)
            salt = welfare.uniqKey
            ppay = self.encryptor.encryptTradePassword(base64.b64decode(user_info.trade_password).decode('utf-8'), salt)
            # buy 秒标
            values = {
                '__hash__': welfare.hash_value,
                'ibnum': welfare.borrowNum,
                'lunchId': '0',  # 红包ID
                'amount': int(math.floor(welfare.available_cash)),
                'p_pay': ppay,
                'user_id': user_info.user_id
            }
            buyinfo = self.buyRequest(values)
            logger.info("标的购买结果：" + buyinfo)
            if buyinfo and 'tnum' in buyinfo:
                session = yatang.Session()
                query = session.query(WelfareInfo).filter(WelfareInfo.ibid == welfare.ibid)
                if query.count() == 0:
                    welfare_info = WelfareInfo.fromWelfare(welfare)
                    session.add(welfare_info)
                    session.commit()
                self.tender_info(welfare.borrowNum, buyinfo['tnum'])
        pass
    
    #用户决定投资金额
    def tenderCF(self, crowdfunding, user_info):
        logger.debug(self.name +" 准备投资众筹" )
        lunchid = "0"
        redpacket = Redpacket(self.opener, crowdfunding.project_id).redpacketListRequest()
        if(redpacket['status'] == 1) :
            if('data' in redpacket and len(redpacket['data'])):
                found = list(filter(lambda d : d['user_constraint'] == self.amount, redpacket['data']))
                if found and len(found) > 0:
                    lunchid = found[0]['id']
        if lunchid == '0':
            logger.info("没有合适的红包")
            return
        salt = crowdfunding.uniqKey
        ppay = self.encryptor.encryptTradePassword(base64.b64decode(user_info.trade_password).decode('utf-8'), salt)
        values = {
                '__hash__': crowdfunding.hash_value,
                'id': crowdfunding.project_id,
                'lunchId': '0',  # 红包ID
                'amount': self.amount,
                'p_pay': ppay,
                'vcode': ''
            }
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASESSL + '/Crowdfunding/checkPay', data.encode(encoding='UTF8'), headers)
        jsonresp = {}
        try:
            response = self.opener.open(req, timeout=30)
            if response.code == 200 :
                resp_data =response.read().decode()
                jsonresp = json.loads(resp_data)
        except URLError as e:
            logger.warn(e)
        except HTTPError as h:
            logger.warn(h)
        except socket.timeout as t:
            logger.warn(t)
        except ValueError: 
            logger.warn("无效的json格式")
            logger.warn(resp_data)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logging.getLogger("app").warn('Unexpected error:',  sys.exc_info()[0])
            
        logger.info("标的购买结果：" + str(jsonresp))
        pass
    
    def buyRequest(self, values):
        logging.info('开始购买标的:' + str(values['amount']))
        data = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASESSL + '/Invest/checkppay', data.encode(encoding='UTF8'), headers)
        jsonresp = {}
        try:
            response = self.opener.open(req, timeout=30)
            if response.code == 200 :
                resp_data =response.read().decode()
                jsonresp = json.loads(resp_data)
        except URLError as e:
            logger.warn(e)
        except HTTPError as h:
            logger.warn(h)
        except socket.timeout as t:
            logger.warn(t)
        except ValueError: 
            logger.warn("无效的json格式")
            logger.warn(resp_data)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logging.getLogger("app").warn('Unexpected error:',  sys.exc_info()[0])
            
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
        req = Request(yatang.YTURLBASESSL + 'Public/tenderinfo', data.encode(encoding='UTF8'), headers)
        jsonresp = {}
        try:
            response = self.opener.open(req, timeout=30)
            if response.code == 200 :
                resp_data =response.read().decode()
                jsonresp = json.loads(resp_data)
        except URLError as e:
            logger.warn(e)
        except HTTPError as h:
            logger.warn(h)
        except socket.timeout as t:
            logger.warn(t)
        except ValueError:
            logger.warn("无效的json格式")
            logger.warn(resp_data)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logging.getLogger("app").warn('Unexpected error:',  sys.exc_info()[0])
           
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
        req = Request(yatang.YTURLBASESSL + 'index.php?s=/Invest/GetBorrowlist', data.encode(encoding='UTF8'), headers)
        aList = []
        try:
            response = self.opener.open(req, timeout=30)
            if response.code == 200:
                resp_data = response.read().decode()
                jsonresp = json.loads(resp_data)

                if(len(typeList) and jsonresp):
                    for loan in jsonresp['data']['Rows']:
                        bt = int(loan['borrow_type'])
                        if bt in typeList:
                            if bt in [1, 9] and int(loan["time_limit"]) == 3:
                                aList.append(loan)
                            else:
                                aList.append(loan)
                else:
                    if jsonresp:
                        aList = jsonresp['data']['Rows']
        except URLError as e:
            logger.warn(e)
        except HTTPError as h:
            logger.warn(h)
        except socket.timeout as t:
            logger.warn(t)
        except ValueError:
            logger.warn("data was not valid JSON")
            logger.warn(resp_data)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logging.getLogger("app").warn('Unexpected error:',  sys.exc_info()[0])
        
        return aList

if __name__ == '__main__':

    from Cookies import Cookies
    from Account import Account
    from Loan import Loan
    c = Cookies()
    cj = c.readCookie('emmaye')
    #c.dumpCookies(cj)
    opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
    install_opener(opener)

    acc = Account(opener)
    accountinfo = acc.accountRequest()
    totalAmount = accountinfo.available

    #i = Invest('emmaye', opener)
    #i.investListRequest()

    assets = Assets(opener)
    assetList = []
    idx = 1
    while len(assetList) < 10:
        assetList.extend(assets.assetRequest(str(idx)))
        idx += idx

    print(assetList)

    for asset in assetList:
        print(asset)
        loan = Loan.loanRequest(opener, asset)
        coupon = Coupon(opener, loan.borrowNum)
        print(coupon.couponListRequest())
    pass