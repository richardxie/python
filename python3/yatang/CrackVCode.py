#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

import cv2
import numpy as np
import json, logging, os, sys, time
from datetime import datetime
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

import yatang

#验证码
class CrackVCode: 
    def __init__(self):
        print("VCode")
    
    @staticmethod
    def preHandle(opener):
        
        t = round(time.time())
        response = opener.open(yatang.YTURLBASESSL + "/GradRedPacket/getVCode")
        content_type = response.info()['Content-Type']
        if(content_type.startswith("image\/")):
            return ""
        
        image_type = content_type[6:]
        dt = datetime.now()
        dtStr = dt.strftime('%Y%m%d%H%M%S')
        with open("../vcode/vcode-%s.%s"%(dtStr, image_type), "wb") as img:
            img.write(response.read())
        
        img = cv2.imread("../vcode/vcode-%s.%s"%(dtStr, image_type))

        #sharpen
        kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], np.float32)  # kernel should be floating point type
        dst = cv2.filter2D(img, -1, kernel)
        cv2.imwrite('../vcode/sharpen.png',dst)
        #res = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
        #
        #边缘检查
        laplacian = cv2.Laplacian(dst,cv2.CV_64F)
        cv2.imwrite('../vcode/laplacian.png',laplacian)

        
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        _,gray = cv2.threshold(gray, 127,255,cv2.THRESH_BINARY)
        cv2.imwrite('../vcode/threshold.png',gray)
        t = (time.time() - t) / 1000
        print("Hand written function time passed in seconds: %s" % t)


def is_grayscale(my_image):
    return len(my_image.shape) < 3

def saturated(sum_value):
    if sum_value > 255:
        sum_value = 255
    if sum_value < 0:
        sum_value = 0

    return sum_value


#锋利
def sharpen(my_image):
    if is_grayscale(my_image):
        height, width = my_image.shape
    else:
        my_image = cv2.cvtColor(my_image, cv2.CV_8U)
        height, width, n_channels = my_image.shape

    result = np.zeros(my_image.shape, my_image.dtype)
    
    for j in range(1, height - 1):
        for i in range(1, width - 1):
            if is_grayscale(my_image):
                sum_value = 5 * my_image[j, i] - my_image[j + 1, i] - my_image[j - 1, i] \
                            - my_image[j, i + 1] - my_image[j, i - 1]
                result[j, i] = saturated(sum_value)
            else:
                for k in range(0, n_channels):
                    sum_value = 5 * my_image[j, i, k] - my_image[j + 1, i, k]  \
                                - my_image[j - 1, i, k] - my_image[j, i + 1, k]\
                                - my_image[j, i - 1, k]
                    result[j, i, k] = saturated(sum_value)
    
    return result


if __name__ == '__main__':
    from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
    from Cookies import Cookies
    c = Cookies()
    cj = c.readCookie('emmaye')
    #c.dumpCookies(cj)
    opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
    install_opener(opener)
    crackVCode = CrackVCode()
    crackVCode.preHandle(opener)