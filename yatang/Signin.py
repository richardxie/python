#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from yatang import Cookies
from urllib2 import install_opener,build_opener,HTTPCookieProcessor
import json, utils, yatang

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
        print "I'm signining"
         #Checkin
        data = json.load(utils.httpRequest(self.opener, yatang.YTURLBASE + "TaskCenter/checkins"))
        
        return data
    