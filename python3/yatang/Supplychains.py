#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

#供应链标
from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
from urllib.parse import urlencode
from marshmallow import Schema, fields, post_load
import json, logging, os, sys, traceback, socket
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

from utils import httpRequest
import yatang

logger = logging.getLogger('app')

class Supplychian:
    def __init__(self, id, borrow_type, name, account, apr, remain, lowest_account, bar, time_limit, award_type, award_rate):
        self.id = id
        self.borrow_type = borrow_type
        self.name = name
        self.account = account
        self.apr = apr
        self.remain = remain
        self.lowest_account = lowest_account
        self.bar = bar
        self.time_limit = time_limit
        self.award_type = award_type
        self.award_rate = award_rate
        pass

    def __repr__(self):
        return '<SupplyChain(标的名称={self.name!r}, 年化收益率={self.apr!s}, 剩余金额={self.remain!s})>'.format(self=self)
    pass

class SupplychianSchema(Schema):
    name = fields.Str()
    id = fields.Str()
    borrow_type = fields.Str()
    account = fields.Str()
    apr = fields.Str()
    remain = fields.Int()
    lowest_account = fields.Str()
    bar = fields.Int()
    time_limit = fields.Str()
    award_type = fields.Str()
    award_rate = fields.Str()

    @post_load
    def make_supplychain(self, data):
        return Supplychian(**data)

    pass

class Supplychains: 
    def __init__(self, opener):
        self.opener = opener
    
    def supplyChainRequest(self):
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
            with self.opener.open(req, timeout=30) as response:
                if response.code == 200:
                    resp_data = response.read().decode()
                    jsonresp = json.loads(resp_data)

                    for loan in jsonresp['data']['Rows']:
                        bt = int(loan['borrow_type'])
                        if bt in [1, 9]:
                            aList.append(loan)
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
    c = Cookies()
    cj = c.readCookie('richardxieq')
    #c.dumpCookies(cj)
    opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
    install_opener(opener)
    a = Supplychains(opener)
    l = a.supplyChainRequest()
    print(l)