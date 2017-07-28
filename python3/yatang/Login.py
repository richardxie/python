#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from http.cookiejar import MozillaCookieJar
from urllib.request import Request, HTTPCookieProcessor, build_opener
from urllib.parse import urlencode
from random import random
import os, sys, time, json

pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

from utils import Encryptor
from Cookies import Cookies
import yatang


class Login: 
    def __init__(self):
        pass
    
    def loginRequest(self, cj, username, password):
        encryptor = Encryptor()
        opener = build_opener(HTTPCookieProcessor(cj))
        ts = time.strftime( "%Y-%m-%d %X", time.localtime() )
        values = {
            'format': 'json',
            'appKey': '00001',
            'v': '1.0',
            'timestamp': ts,
            'method': 'sso.login',
            'origin': 1,
            'source': 1,
            'synUrl' : 'https://jr.yatang.cn/index.php?s=/index/index/*type:1',
            'p': encryptor.encrypt(password, ts),
            'u': username,
            'cookieAge':'30'
        }
        data = urlencode(values).encode('utf-8')
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request( yatang.YTAPIBASESSL + 'yluser', data, headers)
        jsonresp = None
        with opener.open(req) as response:
            jsonresp = json.load(response)

        if(jsonresp and jsonresp['code'] == '0'):
            values = {
                'url': 'https://jr.yatang.cn/index.php?s=/index/index/*type:1'
            }
            data = urlencode(values).encode('utf-8')
            req = Request( yatang.YTURLBASESSL + 'Ajax/setUserCookie', data, headers)
            with opener.open(req) as response:
                if(response.getcode() == 200):
                    return True
                return False
        
        return False

if __name__ == '__main__':
    try:
        YT_USER_AGENT
    except NameError:
        YT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
    
    try:
        YTAPIBASESSL
    except NameError:
        YTAPIBASESSL = 'https://yztapi.yatang.cn/'
    cj = MozillaCookieJar()
    login = Login(); 
    print(login.loginRequest(cj, 'yourname', 'yourpassword'))
    c = Cookies()
    c.dumpCookies(cj)
    cj.save("../cookies/" + 'yourname' + 'Cookie.txt')
    