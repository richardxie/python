#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from yatang import Cookies
from urllib2 import install_opener,build_opener,HTTPCookieProcessor
import json, utils, yatang, logging

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
        logger.debug("I'm signining")
        #Checkin
        response = utils.httpRequest(self.opener, yatang.YTURLBASE + "TaskCenter/checkins")
        #TODO check reponse valid
        data = json.load(response)
        
        return data
    