#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

#资产标
from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
from urllib.parse import urlencode
from marshmallow import Schema, fields, post_load

import json, logging, os, sys, traceback
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

from utils import httpRequest
import yatang
from modules import LoanSchema
from Loan import Loan

logger = logging.getLogger('app')
class Asset:
    def __init__(self, id, borrow_type, name, account, apr, remain, lowest_account, bar, time_limit):
        self.id = id
        self.borrow_type = borrow_type
        self.name = name
        self.account = account
        self.apr = apr
        self.remain = remain
        self.lowest_account = lowest_account
        self.bar = bar
        self.time_limit = time_limit
        pass

    def __repr__(self):
        return '<Asset(标的名称={self.name!r}, 年化收益率={self.apr!s}, 剩余金额={self.remain!s})>'.format(self=self)

class AssetSchema(Schema):
    name = fields.Str()
    id = fields.Str()
    borrow_type = fields.Str()
    account = fields.Str()
    apr = fields.Str()
    remain = fields.Int()
    lowest_account = fields.Str()
    bar = fields.Int()
    time_limit = fields.Str()

    @post_load
    def make_asset(self, data):
        return Asset(**data)

class Assets: 
    def __init__(self, cookie):
        self.cookie = cookie
        if cookie is not None:
            self.opener = build_opener(HTTPCookieProcessor(self.cookie), HTTPRedirectHandler())
            install_opener(self.opener)
    
    def assetRequest(self, page):
        values = {
            'aprrange': 1,   #desc排序
            'selectdate': 2, #1个月标
            'repaystyle': 0,
            'goto_page': '',
            'page_href': '/Financial/getAssetList?&p=' + page
        }
        data = urlencode(values).encode('utf-8')
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
        }
        req = Request(yatang.YTURLBASESSL + 'Financial/getAssetList', data,  headers)
        jsonresp = None
        try:
            response = self.opener.open(req, timeout=300)
            if response.code == 200:
                d = json.loads(response.read().decode())
                jsonresp = AssetSchema().load(d['list'], many=True).data
                #过滤剩余金额过小的标的
                jsonresp = list(filter(lambda x: x.remain > 5000, jsonresp))
        except URLError as e:
            logging.getLogger("app").warn(e)
        except HTTPError as h:
            logging.getLogger("app").warn(h)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logging.getLogger("app").warn('Unexpected error:',  sys.exc_info()[0])

        return jsonresp
    
if __name__ == '__main__':
    from Cookies import Cookies
    c = Cookies()
    cj = c.readCookie('richardxieq')
    c.dumpCookies(cj)

    a = Assets(cj)
    l = a.assetRequest('1')
    print(l)