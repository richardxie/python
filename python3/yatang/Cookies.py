#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

from http.cookiejar import MozillaCookieJar
from urllib.request import HTTPCookieProcessor,build_opener
from random import random
import os, time, json
from utils import Encryptor

class Cookies: 
    BASE_DIR = '../'
    
    def __init__(self, basedir=BASE_DIR):
        self.basedir = basedir
        pass
    
    def readCookies(self):
        cookie_list = []
        cookies = [f for f in os.listdir(self.basedir + 'cookies') if os.path.isfile(self.basedir + 'cookies/' + f)]
        names = map(lambda x: x[0:-10], cookies)
        print(names)
        
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
        names = list(map(lambda x: x[0:-10], cookies))
        
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
        opener.open(YTURLBASE + 'NewLogin/index/referer')
        for _ in range(0, 3):
            try:
                verifycode = self.verifyCode(opener).strip()
                encryptedpwd = Encryptor().encryptPassword(password, verifycode)
                print (verifycode, str(len(verifycode)), encryptedpwd)
                if(self.loginRequest(opener, username, encryptedpwd)):
                    self.dumpCookies(cj)
                    cj.save(self.basedir + "cookies/" + username + 'Cookie.txt')
                break;
            except Exception as e:
                print (e)
                continue
        return cj

    def dumpCookies(self, cj):
        aDict = {}
        for ck in cj:
            print (ck.name + ":" + ck.value)
            aDict[ck.name] = ck.value
        return aDict

if __name__ == '__main__':
    cookies = Cookies(); 
    print(cookies.readCookies())