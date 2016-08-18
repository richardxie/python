#!/usr/bin/python2.7
#！-*- coding: utf-8 -*-

DEBUG = True
USECOOKIES = False
YTURLBASE = "http://jr.yatang.cn/"
YTURLBASESSL = "https://jr.yatang.cn/"
YT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
BASEDIR = '/Users/wuqh/'
#BASEDIR='./'
import urllib, urllib2, cookielib,json,time
import smtplib
import os, random
import lxml.html.soupparser as soupparser
import tesserpy
import cv2
import PyV8
from email.mime.text import  MIMEText
from email.header import Header

def dumpCookies(cj):
    for ck in cj:
        print ck.name + ":" + ck.value
    pass

def verifyCode(opener):
    response = opener.open(YTURLBASE + "index.php?s=/NewLogin/verify/%f"%(random.random()))
    content_type = response.info()['Content-Type']
    if(content_type.startswith("image\/")):
        return ""
    
    image_type = content_type[6:]
    with open(BASEDIR + "images/verifyCode." + image_type, "w" ) as img:
        img.write(response.read())
    tesser = tesserpy.Tesseract('/usr/local/share/tessdata/', language="eng")
    tesser.tessedit_char_whitelist = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    img = cv2.imread(BASEDIR + "images/verifyCode.png", cv2.IMREAD_GRAYSCALE)
    tesser.set_image(img);
    page_info = tesser.orientation();
    return tesser.get_utf8_text()

def encrypt(password, verifyCode):
    with PyV8.JSContext() as jsctx:
        with open("encrypt.js") as jsfile:
            jsctx.eval(jsfile.read())
            encryptFunc = jsctx.locals.encrypt;
            pwd = encryptFunc(password, verifyCode)
    return pwd

def loginRequest(opener, username, password):
    values = {
        'cookietime':2880,
        'password':password,
        'username':username
    }
    data = urllib.urlencode(values)
    headers = {
        'User-Agent': YT_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    req = urllib2.Request(YTURLBASE + 'index.php?s=/new_login/checklogin', data, headers)
    response = opener.open(req)
    #resp = response.read().encode("utf-8")
    jsonresp = json.load(response)
    if(jsonresp['status'] == 1):
        return True
    
    return False

def login(username, password):
    cj = cookielib.MozillaCookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.open(YTURLBASE + 'NewLogin')
    for i in range(0, 3):
        try:
            verifycode = verifyCode(opener).strip()
            encryptedpwd = encrypt(password, verifycode)
            print verifycode, str(len(verifycode)), encryptedpwd
            if(loginRequest(opener, username, encryptedpwd)):
                dumpCookies(cj)
                cj.save(BASEDIR + "cookies/" + username + 'Cookie.txt')
                break;
        except:
            continue
    pass

def user_info(html):
    dom = soupparser.fromstring(html)
    user_element =  dom.xpath('/html/body/div[7]/div/div[2]/div[1]/dl/dd[1]/span')
    user = user_element[0].text
    level_ele =  dom.xpath('/html/body/div[7]/div/div[2]/div[1]/dl/dd[5]/span/img')
    level = level_ele[0].get('src').split('/')[-1][0:-4]
    return (user, level)


def send_mail(mail_list):
    #send email
    mail_host = 'smtp.163.com'
    mail_port = 465
    mail_user = 'test_shanlin@163.com'
    mail_pwd = '111111a'
    mail_receiver = ['13524470327@139.com','richard_xieq@foxmail.com']
    mail_to =','.join(mail_receiver)
    message ='<h3>本次雅堂签到的相关信息</h3>'
    message += '<ul>'
    for value in mail_list:
        msg = '<li>%s:v%s雅堂签到：%s</li>'%(value['user'][0], value['user'][1], value['data']['data']['tomorrow'])
        message += msg;
    message += '</ul>'
    msg = MIMEText(message,  _subtype='html', _charset='utf-8');
    msg['to'] = mail_to;
    msg['from'] = mail_user;
    msg['Subject'] = Header(u'雅堂签到', 'UTF-8').encode()
    server = smtplib.SMTP_SSL(mail_host, mail_port)
    server.set_debuglevel(1)
    server.login(mail_user, mail_pwd)
    server.sendmail(mail_user, mail_to, msg.as_string())
    server.quit()

def httpRequest(opener, url):
    request = urllib2.Request(url)
    response = opener.open(request)
    return response

def readCookies():
    cookies = [file for file in os.listdir(BASEDIR + 'cookies') if os.path.isfile(BASEDIR + 'cookies/' + file)]

    mail_list = []
    for cookie in cookies:
        cj = cookielib.MozillaCookieJar()
        cj.load(BASEDIR + 'cookies/' + cookie)
        for ck in cj:
            ck.expires = int(time.time() + 30 * 24 * 3600)
        cj.save(BASEDIR + "cookies/" + cookie)
    
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    
        #User info
        uinfo = user_info(httpRequest(opener, YTURLBASESSL + "Account/MyNews/title/MMHPage").read())
        
        #Checkin
        data = json.load(httpRequest(opener, YTURLBASE + "TaskCenter/checkins"))
        
        print data['data']
        mail_list.append({'user':uinfo, 'data': data})
        opener.close()
    listlen = len(mail_list)
    if(listlen > 0):
        send_mail(mail_list)
    return listlen
    
def main():
    if(readCookies()==0):
        username = raw_input(u"用户名：")
        password = raw_input(u'密码：')
        login(username, password)
    

if __name__ == '__main__':
    main()

