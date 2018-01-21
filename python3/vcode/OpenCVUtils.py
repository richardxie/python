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

#验证码
class OpenCVUtils:
    def __init__(self):
        print("OpenCVUtils")
    
    @staticmethod
    def preHandle(opener):
        
        t = round(time.time())
        img = cv2.imread("../vcode/vcode-%s.%s"%(dtStr, image_type))

        kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]], np.float32)  # kernel should be floating point type
        dst = cv2.filter2D(img, -1, kernel)
        cv2.imwrite('../vcode/sharpen.png',dst)
        #res = cv2.resize(img,None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        _,gray = cv2.threshold(gray, 127,255,cv2.THRESH_BINARY)
        cv2.imwrite('../vcode/threshold.png',gray)
        t = (time.time() - t) / 1000
        print("Hand written function time passed in seconds: %s" % t)


    @staticmethod
    def is_grayscale(my_image ):
        return len(my_image.shape) < 3

    @staticmethod
    def saturated(sum_value ):
        if sum_value > 255:
            sum_value = 255
        if sum_value < 0:
            sum_value = 0

        return sum_value


    #锋利
    @staticmethod
    def sharpen( my_image ):
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

    #颜色查找
    @staticmethod
    def findColor( my_image ):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(my_image, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV
        blue = np.uint8([[[51,19,54 ]]])
        hsv_blue = cv2.cvtColor(blue,cv2.COLOR_BGR2HSV)
        blue_flat = hsv_blue.flatten()
        lower_blue = blue_flat + np.array([-10,-5,0], dtype = np.uint8)
        upper_blue = blue_flat + np.array([10,5,0], dtype = np.uint8)

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(my_image, my_image, mask= mask)
        cv2.imwrite('colorspaxe.png', res)
        pass

    #轮廓查找
    @staticmethod
    def findContours( my_image ):
        imgray = cv2.cvtColor(my_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 127, 255, 0)
        cv2.imwrite('imgray.png', thresh)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imwrite('im2.png', im2)
        #cnt = contours[4]
        #cv2.drawContours(img, [cnt], 0, (0,255,0), 3)
        cv2.drawContours(my_image, contours, 0, (0,255,0), 3)
        cv2.imwrite('findContours.png', im2)
        pass

    #边缘查找
    @staticmethod
    def findEdge( my_image ):
        laplacian = cv2.Laplacian(my_image,cv2.CV_64F, ksize = 3)
        res = cv2.bitwise_and(my_image, my_image, mask= laplacian)
        cv2.imwrite('laplacian.png',res)
        """
        sobelx = cv2.Sobel(my_image,cv2.CV_64F,1,0,ksize=3)
        cv2.imwrite('sobelx.png',sobelx)
        sobely = cv2.Sobel(my_image,cv2.CV_64F,0,1,ksize=3)
        cv2.imwrite('sobely.png',sobely)
        """
       
        return laplacian

    @staticmethod
    def ocr( my_image ):
        imgray = cv2.cvtColor(my_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(imgray, 90, 255, cv2.THRESH_BINARY)
        img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        drawing = np.zeros(imgray.shape,np.uint8)
        filtered = []
        for cnt in contours:
            color = np.random.randint(0,255,(3)).tolist()  # Select a random color
            bx,by,bw,bh = cv2.boundingRect(cnt)
            (cx,cy),radius = cv2.minEnclosingCircle(cnt)
            if bw > 5:
                filtered.append(cnt)
                cv2.drawContours(drawing,[cnt],0,color,1)
                cv2.rectangle(drawing,(bx,by),(bx+bw,by+bh),(255,0,0),1) # draw rectangle in blue color)
            

            
        
        #cv2.drawContours(drawing, filtered, -1, (0,255,0), 3)
        cv2.imwrite('ocr.png', drawing)

        pass
    
    @staticmethod
    def histogram( my_image ):
        '''
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([img],[i],None,[256],[0,256])
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(histr)
            plt.plot(histr,color = col)
            plt.xlim([0,256])
        plt.show()
        '''

        b,g,r = cv2.split(my_image)
        hist = cv2.calcHist([b],[0],None, [256], [0,256])
        _, maxVal, _, maxLoc = cv2.minMaxLoc(hist)

        mask = np.zeros(my_image.shape, my_image.dtype)
        dst = cv2.inRange(b, maxLoc[1] - 10, maxLoc[1] + 10)
        cv2.imwrite('dst.png', dst)
        pass

if __name__ == '__main__':
    img = cv2.imread("vcode-20171220164034.png")
    opencv = OpenCVUtils()
    #opencv.findColor( img )
    img = opencv.ocr( img )
    #opencv.findContours( img )