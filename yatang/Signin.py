#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from yatang import Cookies
from urllib2 import install_opener,build_opener,HTTPCookieProcessor
import json, utils, yatang, logging
from modules import SigninInfo
from datetime import datetime

logger = logging.getLogger("app")

class Signin:

    def __init__(self, cookie = None, name = None, password = None):
        self.cookie = cookie
        self.name = name
        self.passwd = password
        if(cookie is not None):
            self.opener = build_opener(HTTPCookieProcessor(self.cookie))
            install_opener(self.opener)
        else:
            self.cookie = Cookies().genCookie(name, password)
            self.opener = build_opener(HTTPCookieProcessor(self.cookie))
            install_opener(self.opener)
    
    def signin(self):
        logger.info(self.name + " is signining")
        session = yatang.Session()
        query = session.query(SigninInfo).filter(SigninInfo.name == self.name, SigninInfo.website=='yt')
        #chekc already siginin today      
        if query.count() != 0:
            signin_info = query.one()
            if signin_info.signin_date.date() == datetime.today().date():
                logger.info(" Dear %s, Today(%s) already signined 雅堂"%(self.name, signin_info.signin_date.strftime('%Y-%m-%d')))
                return
        #Checkin
        response = utils.httpRequest(self.opener, yatang.YTURLBASE + "TaskCenter/checkins")
        if response and response.code == 200:
            data = json.load(response)
            
            if(query.count() == 0):
                import uuid
                signin_info = SigninInfo(
                            id=str(uuid.uuid1()),                             
                            name=self.name,
                            website='yt'
                        )
                session.add(signin_info)
                session.commit()
            else:
                signin_info.prev_signin_date = signin_info.signin_date
                signin_info.update_date = signin_info.signin_date = datetime.now()
                session.commit()
                pass
        
        return data
    