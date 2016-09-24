#!/usr/bin/python2.7
#！-*- coding: utf-8 -*-

DEBUG = True
USECOOKIES = False
TZJURLBASE = "https://account.touzhijia.com/signin.html"
TZJURLBASESSL = "https://account.touzhijia.com/"
TZJ_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
#BASEDIR = '/Users/wuqh/'
BASEDIR='./'
import urllib, urllib2, cookielib,json,base64
import smtplib
import os
from email.mime.text import  MIMEText
from email.header import Header
import locale, sys
import pdb

def initSys():
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    pass
    
def dumpCookies(cj):
    for ck in cj:
        print ck.name + ":" + ck.value
    pass

def signin(opener):
	  req = urllib2.Request(TZJURLBASESSL + 'shop/signin')
	  response = opener.open(req)
	  pdb.set_trace()
	  jsonData = json.load(response)
	  print jsonData
	  pass

def loginRequest(opener, username, password):
    values = {
        'remeber':1,
        'password':password,
        'username':username
    }
    data = urllib.urlencode(values)
    headers = {
        'User-Agent': TZJ_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    req = urllib2.Request(TZJURLBASESSL + 'signin.html', data, headers)
    pdb.set_trace()
    response = opener.open(req)
    #resp = response.read().encode("utf-8")
    if(response.getcode() == 200):
        return True
    
    return False

def login(username, password):
    cj = cookielib.MozillaCookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.open(TZJURLBASESSL + 'signin.html')
    for i in range(0, 3):
        try:
            encryptedpwd = base64.b64encode(password)
            if(loginRequest(opener, username, encryptedpwd)):
                dumpCookies(cj)
                cj.save(BASEDIR + "tzj/cookies/" + username + 'Cookie.txt')
                signin(opener)
                break;
        except:
            continue
    pass


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
        msg = '<li>%s:v%s雅堂签到：%s</li>'%(value['user']['username'], value['user']['level'], value['data']['data']['tomorrow'])
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



def main():
    initSys()
    
    username = raw_input(u"用户名：")
    password = raw_input(u'密码：')
    if(len(password) > 0):
    	login(username, password)
    

if __name__ == '__main__':
    main()

