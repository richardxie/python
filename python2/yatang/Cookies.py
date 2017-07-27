#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from cookielib import MozillaCookieJar
from urllib2 import HTTPCookieProcessor,Request,build_opener
from random import random
import yatang
import urllib
import os, time, json
import tesserpy, cv2
from utils import encryptPassword

class Cookies: 
    BASE_DIR = '../'
    
    def __init__(self, basedir=BASE_DIR):
        self.basedir = basedir;
        pass
    
    def readCookies(self):
        cookie_list = []
        cookies = [f for f in os.listdir(self.basedir + 'cookies') if os.path.isfile(self.basedir + 'cookies/' + f)]
        names = map(lambda x: x[0:-10], cookies)
        print names
        
        for _, cookie in enumerate(cookies):
            cj = MozillaCookieJar()
            cj.load(self.basedir + 'cookies/' + cookie)
            for ck in cj:
                ck.expires = int(time.time() + 30 * 24 * 3600)
            cj.save(self.basedir + "cookies/" + cookie)
            cookie_list.append(cj)
        return cookie_list
    
    def readCookie(self, name):
        cookies = [f for f in os.listdir(self.basedir + 'cookies') if os.path.isfile(self.basedir + 'cookies/' + f)]
        names = map(lambda x: x[0:-10], cookies)
        
        cj = MozillaCookieJar()
        if name not in names:
            return cj
        
        cookie_file_name = self.basedir + 'cookies/' + name + 'Cookie.txt'
        cj.load(cookie_file_name)
        for ck in cj:
            ck.expires = int(time.time() + 30 * 24 * 3600)
        cj.save(cookie_file_name)
        return cj
    
    def genCookie(self, username, password):
        cj = MozillaCookieJar();
        opener = build_opener(HTTPCookieProcessor(cj))
        opener.open(yatang.YTURLBASE + 'NewLogin')
        for _ in range(0, 3):
            try:
                verifycode = self.verifyCode(opener).strip()
                encryptedpwd = encryptPassword(password, verifycode)
                print verifycode, str(len(verifycode)), encryptedpwd
                if(self.loginRequest(opener, username, encryptedpwd)):
                    self.dumpCookies(cj)
                    cj.save(self.basedir + "cookies/" + username + 'Cookie.txt')
                break;
            except Exception, e:
                print e
                continue
        return cj

    def dumpCookies(self, cj):
        aDict = {}
        for ck in cj:
            print (ck.name + ":" + ck.value)
            aDict[ck.name] = ck.value
        return aDict
    
    def verifyCode(self, opener):
        response = opener.open(yatang.YTURLBASE + "index.php?s=/NewLogin/verify/%f" % (random()))
        content_type = response.info()['Content-Type']
        if(content_type.startswith("image\/")):
            return ""
        
        image_type = content_type[6:]
        with open(self.basedir + "images/verifyCode." + image_type, "w") as img:
            img.write(response.read())
        import platform
        if platform.system() == 'Darwin':
            tesser = tesserpy.Tesseract('/usr/local/share/tessdata/', language="eng")
        else:
            tesser = tesserpy.Tesseract("/usr/share/tesseract-ocr/tessdata/", language="eng")
        tesser.tessedit_char_whitelist = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        img = cv2.imread(self.basedir + "images/verifyCode.png", cv2.IMREAD_GRAYSCALE)
        tesser.set_image(img);
        page_info = tesser.orientation();
        print page_info
        return tesser.get_utf8_text()
    
    def loginRequest(self, opener, username, password):
        values = {
            'cookietime':2880,
            'password':password,
            'username':username
        }
        data = urllib.urlencode(values)
        headers = {
            'User-Agent': yatang.YT_USER_AGENT,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        req = Request(yatang.YTURLBASE + 'index.php?s=/new_login/checklogin', data, headers)
        response = opener.open(req)
        #resp = response.read().encode("utf-8")
        jsonresp = json.load(response)
        if(jsonresp and jsonresp['status'] == 1):
            return True
        
        return False
