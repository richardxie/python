#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
from urllib.parse import urlencode
import json, logging, os, sys
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

import yatang
from Cookies import Cookies

#投资众筹用红包
class Redpacket: 
    def __init__(self, opener, projectID="71"):
        self.projectID = projectID
        self.opener = opener

    def __repr__(self):
        return "<Redpacket(项目编号='%s')>" % (
                self.projectID)

    def redpacketListRequest(self):
        values = {
            'investMoney': '15000',
            'projectId': self.projectID,
            'pageNum': '1'
        }
        postData = urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
        req = Request(url = yatang.YTURLBASESSL + 'Crowdfunding/ajaxGetUserRedPacket', data= postData.encode(encoding='UTF8'),  headers=headers, method='POST')
        jsonresp = None
        try:
            with self.opener.open(req, timeout=30) as response:
                if response.code == 200:
                    jsonresp = json.loads(response.read().decode())
        except URLError as e:
            logging.getLogger("app").warn(e)
        except HTTPError as h:
            logging.getLogger("app").warn(h)
        except:
            print ("Unexpected error:", sys.exc_info()[0])
            logging.getLogger("app").warn('Unexpected error:',  sys.exc_info()[0])

        return jsonresp

if __name__ == '__main__':
    c = Cookies()
    cj = c.readCookie('richardxieq')
    #c.dumpCookies(cj)
    opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
    install_opener(opener)
    c = Redpacket(opener)
    print(c.redpacketListRequest())
    pass