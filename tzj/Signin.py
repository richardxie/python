#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from urllib2 import build_opener, HTTPCookieProcessor, Request, URLError, HTTPError
from urllib import urlencode
from cookielib import MozillaCookieJar
from utils import EmailUtils
import json, logging, base64
import tzj, yatang
from yatang.modules import SigninInfo, UserInfo
from datetime import datetime

DEBUG = True
BASEDIR = "./"

logger = logging.getLogger("app")

class Signin:

    def __init__(self, name):
        self.username = name
        session = yatang.Session()
        query = session.query(UserInfo).filter(UserInfo.name == self.username, UserInfo.website=='tzj')
        if query.count() != 0:
            self.password = base64.b64decode(query.one().password)
            print self.password
        
    def signin(self):
        #Check siginin today
        session = yatang.Session()
        query = session.query(SigninInfo).filter(SigninInfo.name == self.username, SigninInfo.website=='tzj')
        if query.count() != 0:
            signin_info = query.one();
            if signin_info.signin_date.date() == datetime.today().date():
                logger.info(" Dear %s, Today(%s) already signined 投之家."%(self.username, signin_info.signin_date.strftime('%Y-%m-%d')))
                return
            
        if self.login() :
            return self.signinRequest()
        else:
            return None
    
    def signinRequest(self):
        logger.info(self.username + "is signining in 投之家")
        headers = {
            'User-Agent': tzj.TZJ_USER_AGENT,
            'Content-Type': 'application/json; charset=UTF-8'
        }
        req = Request(url = tzj.TZJURLBASESSL + 'checkin', headers=headers)
        response = self.opener.open(req)

        if response.code == 200:
            jsonData = json.load(response)
            logger.info(jsonData)
            ###{u'info': {u'Username': u'YfzGvk6Ih6', u'SignCount': 1, 
            ###u'LastSignDate': u'2016-09-07T14:26:38+08:00', u'Score': 1, 
            ###u'SignInReward': {u'1': 1, u'3': 5, u'2': 3, u'5': 9, u'4': 7, u'7': 15, u'6': 11}}, u'ret': 1}
            session = yatang.Session()
            query = session.query(SigninInfo).filter(SigninInfo.name == self.username, SigninInfo.website=='tzj')
            if(query.count() == 0):
                import uuid
                signinf_info = SigninInfo(
                                id=str(uuid.uuid1()),                             
                                   name=self.username,
                                   website='tzj',
                                   signin_date = datetime.now()
                            )
                session.add(signinf_info)
                session.commit()
            else:
                signin_info = query.one()
                signin_info.prev_signin_date = signin_info.signin_date
                signin_info.signin_date = datetime.now()
                session.commit()
            
            if(jsonData['ret'] == 1):
                EmailUtils().send_mail(jsonData)
            return jsonData
        else:
            return {"errorCode":"000", "errorMsg":"http request errorcode" + response.code}
    
    def login(self):
        cj = MozillaCookieJar();
        self.opener = build_opener(HTTPCookieProcessor(cj))
        self.opener.open(tzj.TZJURLBASESSL + 'signin.html')
        res = False
        for _ in range(0, 3):
            try:
                if(self.loginRequest()):
                    cj.save(BASEDIR + "cookies/tzj/" + self.username + 'Cookie.txt')
                    res = True
                    break;
            except Exception,e:
                print e
                continue
        return res
    
    def loginRequest(self):
        logger.info(self.username + ' wants to login 投之家.')
        values = {
            'next':'https://account.touzhijia.com',
            'remember':'on',
            'password':self.password,
            'userID':self.username
        }
        data = urlencode(values)
        headers = {
            'User-Agent': tzj.TZJ_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(tzj.TZJURLBASESSL + 'signin', data, headers)
        try:
            response = self.opener.open(req, timeout = 30)
    
            if(response.getcode() == 200):
                return True
        except URLError, e:
            logger.warn(e)
        except HTTPError as h:
            logger.warn(h)
        
        return False