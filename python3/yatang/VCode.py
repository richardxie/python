#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

import cv2
import numpy as np
import json, logging, os, sys
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

import yatang

#验证码
class VCode: 
    def __init__(self):
        print("VCode")
    
    @staticmethod
    def preHandle(opener):
        '''
        response = opener.open(yatang.YTURLBASESSL + "/GradRedPacket/getVCode")
        content_type = response.info()['Content-Type']
        if(content_type.startswith("image\/")):
            return ""
        
        image_type = content_type[6:]
        with open("../vcode/vcode1." + image_type, "wb") as img:
            img.write(response.read())
        '''
        img = cv2.imread('../vcode/vcode1.png')

        res = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
        
        res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
        _,res = cv2.threshold(res, 127,255,cv2.THRESH_BINARY)
        cv2.imwrite('../vcode/threshold.png',res)


if __name__ == '__main__':
    from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
    from Cookies import Cookies
    c = Cookies()
    cj = c.readCookie('emmaye')
    #c.dumpCookies(cj)
    opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
    install_opener(opener)
    vcode = VCode()
    vcode.preHandle(opener)