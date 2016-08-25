#!/usr/bin/python2.7
#！-*- coding: utf-8 -*-

DEBUG = True
USECOOKIES = False
YTURLBASE = "http://jr.yatang.cn/"
YTURLBASESSL = "https://jr.yatang.cn/"
YT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
#BASEDIR = '/Users/wuqh/'
BASEDIR='./'
import urllib, urllib2, cookielib,json,time
import smtplib
import os, random
import lxml.html.soupparser as soupparser
import tesserpy
import cv2
import PyV8
from email.mime.text import  MIMEText
from email.header import Header
import pymysql
import locale, sys

def initSys():
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    pass
    
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
    return {'username': user,
            'level': int(level)
            }

def account_info(html):
    dom = soupparser.fromstring(html)
    user_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/div[1]/div[1]/p[2]/b')
    user_name = user_ele[0].text
    balance_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/ul[1]/li[1]/p/span')
    account_balance = money(balance_ele[0].text)
    income_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/ul[1]/li[3]/p/span')
    account_income = money(income_ele[0].text)
    collection_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/ul[1]/li[4]/p/span')
    account_collection = money(collection_ele[0].text)
    payment_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/ul[2]/li[4]/p/span')
    account_payment = money(payment_ele[0].text)
    account_info = {'user':user_name,
                    'balance': account_balance,
                    'income': account_income,
                    'collection': account_collection,
                    'payment': account_payment
                    }
    return account_info

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

def httpRequest(opener, url):
    request = urllib2.Request(url)
    response = opener.open(request)
    return response

def readCookies():
    cookies = [file for file in os.listdir(BASEDIR + 'cookies') if os.path.isfile(BASEDIR + 'cookies/' + file)]
    names = map(lambda x: x[0:-10],cookies)
    mail_list = []
    for index, cookie in enumerate(cookies):
        cj = cookielib.MozillaCookieJar()
        cj.load(BASEDIR + 'cookies/' + cookie)
        for ck in cj:
            ck.expires = int(time.time() + 30 * 24 * 3600)
        cj.save(BASEDIR + "cookies/" + cookie)
    
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
    
        #User info
        uinfo = user_info(httpRequest(opener, YTURLBASESSL + "Account/MyNews/title/MMHPage").read())
        uinfo['id'] = findUserDB(names[index])['id']
        
        #Account info
        account = account_info(httpRequest(opener, YTURLBASESSL + "index.php?s=/Account/").read())
        
        #update database
        updateAccountDB(uinfo, account)
        #Checkin
        data = json.load(httpRequest(opener, YTURLBASE + "TaskCenter/checkins"))
        
        print data['data']
        mail_list.append({'user':uinfo, 'data': data})
        opener.close()
    listlen = len(mail_list)
    if(listlen > 0):
        send_mail(mail_list)
    return listlen 
    
def connectDB():
    connection = pymysql.connect(host='192.16.2.139',
                                user='admin',
                                password='admin',
                                db='test',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = 'insert into `user` (`email`, `password`) values (%s, %s)'
            cursor.execute(sql, ("richardxieq", "admin"))
        connection.commit()
        
        with connection.cursor() as cursor:
            sql = 'select `id`, `password` from `user`'
            cursor.execute(sql)
            for r in cursor.fetchall():
                print r

    finally:
        connection.close()
        
def findUserDB(username):
    connection = pymysql.connect(host='192.16.2.139',
                                user='admin',
                                password='admin',
                                db='test',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = 'select `id`, `name`, `level` from `user` where name=%s';
            effected_row = cursor.execute(sql,(username))
            assert(cursor.rowcount == 1)
            return cursor.fetchone()

    finally:
        connection.close()

def updateAccountDB(user, account):
    connection = pymysql.connect(host='192.16.2.139',
                                user='admin',
                                password='admin',
                                db='test',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = 'insert into `user` (`name`, `level`) values (%s, %s) on duplicate key update `level` = case when values(`level`) < level then level else values(`level`) end'
            effected_row = cursor.execute(sql,(user['username'], user['level']))
        connection.commit()
        
        with connection.cursor() as cursor:
            sql = 'insert into `account` (`user_id`, `name`, `balance`, `income`, `collection`, `payment`) values (%s, %s, %s, %s, %s, %s) on duplicate key update `name` = values(name)'
            effected_row = cursor.execute(sql,(user['id'], user['username'], account['balance'], account['income'], account['collection'], account['payment']))
        connection.commit()

    finally:
        connection.close()
    pass      

def money(string):
    locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    sym = locale.localeconv()['currency_symbol']
    if sym:
        string = string.replace(sym, '')
    ts = locale.localeconv()['thousands_sep']
    if ts:
        string = string.replace(ts, '') #next, replace the decimal point with a 
    dd = locale.localeconv()['decimal_point']
    if dd:
        string = string.replace(dd, '.') #finally, parse the string
    return float(string)   

def main():
    initSys()
#     connectDB();
    
    if(readCookies()==0):
        username = raw_input(u"用户名：")
        password = raw_input(u'密码：')
        if(len(password) > 0):
            login(username, password)
    

if __name__ == '__main__':
    main()

