#!/usr/bin/python3
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
import lxml.html.soupparser as soupparser
from lxml.html import html5parser
from lxml.html import html5parser
from html5lib import HTMLParser,treebuilders
from email.mime.text import  MIMEText
from email.header import Header
import os, locale, sys, threading
import logging
import PyV8

def initSys():
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    pass
    
def dumpCookies(cj):
    for ck in cj:
        print (ck.name + ":" + ck.value)
    pass

def encrypt(password, verifyCode):
    with PyV8.JSContext() as jsctx:
        with open("encrypt.js") as jsfile:
            jsctx.eval(jsfile.read())
            encryptFunc = jsctx.locals.encrypt2;
            pwd = encryptFunc(password, verifyCode)
    return pwd
	
def chest_info(html):
    try:
        dom = soupparser.parse(html, "html5lib")
        return chest_info_dom(dom)
    except:    
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser = parser)
        return chest_info_dom(dom)

def chest_info_dom(document):
    available_redPacket_element =  document.xpath('/html/body/div[6]/div/div/div/div[3]/span')
    available_redPacket = available_redPacket_element[0].text.split(":")[1]
    chest_list_element = document.xpath('/html/body/div[6]/div/div/div/div[4]/div')
    type(chest_list_element)
    len(chest_list_element)
    pass

def welfare_info(html):
    print "welfare_info start."
    parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
    dom = html5parser.parse(html, parser = parser)
    
    ibid_element = dom.xpath('//*[@class="amountt_input"]')
    ibid = ibid_element[0].attrib['dataid']
    borrowNum_element = dom.xpath("//*[@id=\"iborrownumid_"+ibid+"\"]")
    borrowNum = borrowNum_element[0].attrib['value']
    borrowType_element = dom.xpath('//*[@id="iborrowtype_'+ibid+'"]')
    borrowType = borrowType_element[0].attrib['value']
    hash_element = dom.xpath("/html/body/div[3]/div[4]/div[2]/div[3]/form/input[2]")
    hash =  hash_element[0].attrib["value"]

    uniqkey_element = dom.xpath("//*[@id='uniqKey']")
    uniqKey = uniqkey_element[0].attrib['value']

    cash_element = dom.xpath('//*[@id="ktmje_'+ibid+'"]')
    cash = money(cash_element[0].attrib["value"])
    return {
        "__hash__":hash,
        "ibid":ibid,
        'borrowType':borrowType,
        "borrowNum":borrowNum,
        "available_cash":cash,
	"uniqKey":uniqKey
        }
    pass

def loan_info(html): 
    parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
    dom = html5parser.parse(html, parser = parser)
    
    ibid_element = dom.xpath('//*[@id="ibid"]')
    ibid = ibid_element[0].attrib['value']
    borrowNum_element = dom.xpath("//*[@id=\"iborrownumid\"]")
    borrowNum = borrowNum_element[0].attrib['value']
    borrowType_element = dom.xpath('//*[@id="iborrowtype"]')
    borrowType = borrowType_element[0].attrib['value']
    hash_element = dom.xpath("/html/body/div[2]/div[3]/form/input")
    hash =  hash_element[0].attrib["value"]

    cash_element = dom.xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/span[2]")
    cash = money(cash_element[0].text.replace('元',''))
    return {
        "__hash__":hash,
        "ibid":ibid,
        'borrowType':borrowType,
        "borrowNum":borrowNum,
        "available_cash":cash
        }

def dumpInvestList(jsonresp):
    if(jsonresp['status'] == 1):
        if(int(jsonresp['data']['Total']) > 0):
            list = jsonresp['data']['Rows']
            for loan in list:
                print (loan['borrow_type']) #借款类型
                print (loan['id']) #借款ID
                print (loan['name']) #借款名
                print (loan['apr']) #借款利率
                print (loan['remain']) #借款剩余余额
    pass

def investListRequest(opener, typeList):
    values = {
        'mode':1,
        'tpage[page]':1,
        'tpage[size]':20
    }
    data = urllib.urlencode(values)
    headers = {
        'User-Agent': YT_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    req = urllib2.Request(YTURLBASE + 'index.php?s=/Invest/GetBorrowlist', data.encode(encoding='UTF8'), headers)
    response = opener.open(req)

    jsonresp = json.loads(response.read().decode())
    if(len(typeList)):
        list = []
        for loan in jsonresp['data']['Rows']:
            if int(loan['borrow_type']) in typeList:
                list.append(loan)
        return list
    else:
        return jsonresp['data']['Rows']
    
def  dumpCouponList(jsonresp):
    print(jsonresp)
    if(jsonresp['status'] == 1):
        print(jsonresp['withdrawalCash'])
        for coupon in jsonresp['data']:
            print(coupon)
        pass
    else:
        print('coupou error.')
    pass

def couponListRequest(opener, borrowNum):
    values = {
        'investMoney':'',
        'borrowNum': borrowNum,
        'pageNum':1
    }
    data = urllib.urlencode(values)
    headers = {
        'User-Agent': YT_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    req = urllib.Request(YTURLBASE + 'Ajax/getUserCoupon', data.encode(encoding='UTF8'), headers)
    response = opener.open(req)

    jsonresp = json.loads(response.read().decode())
    dumpCouponList(jsonresp)
    return jsonresp

def matchCouponOnLoan(coupons, loan):
    
    pass

def tender_info(opener, borrow_num, tnum):
    values = {
        'borrow_num':borrow_num,
        'tnum': tnum
    }
    data = urllib.urlencode(values)
    headers = {
        'User-Agent': YT_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    req = urllib2.Request(YTURLBASE + 'Public/tenderinfo', data.encode(encoding='UTF8'), headers)
    response = opener.open(req)

    jsonresp = json.loads(response.read().decode())
    logging.debug(jsonresp)
    return jsonresp

def buyRequest(opener, values):
    print 'buy start.'
    data = urllib.urlencode(values)
    headers = {
        'User-Agent': YT_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    req = urllib2.Request(YTURLBASE + 'Invest/checkppay', data.encode(encoding='UTF8'), headers)
    response = opener.open(req)
    jsonresp = json.loads(response.read().decode())
    print jsonresp
    logging.debug(jsonresp)
    return jsonresp

def send_mail(mail_list):
    #send email
    mail_host = 'smtp.163.com'
    mail_port = 465
    mail_user = 'test_shanlin@163.com'
    mail_pwd = '111111a'
    mail_receiver = ['13524470327@139.com','richard_xieq@foxmail.com']
    mail_to =','.join(mail_receiver)
    message ='<h3>本次雅堂購買的相关信息</h3>'
    message += '<ul>'
    for value in mail_list:
        msg = '<li>%s:v%s雅堂购买：%s</li>'%(value['user']['username'], value['user']['level'], value['data']['data']['tomorrow'])
        message += msg;
    message += '</ul>'
    msg = MIMEText(message,  _subtype='html', _charset='utf-8');
    msg['to'] = mail_to;
    msg['from'] = mail_user;
    msg['Subject'] = Header('雅堂购买', 'UTF-8').encode()
    server = smtplib.SMTP_SSL(mail_host, mail_port)
    server.set_debuglevel(1)
    server.login(mail_user, mail_pwd)
    server.sendmail(mail_user, mail_to, msg.as_string())
    server.quit()

def httpRequest(opener, url):
    request = urllib2.Request(url)
    try:
        response = opener.open(request)
    except urllib.error.HTTPError as e:
        print(e.code())
    
    return response
    
def buy_func(opener):
    print("buy function", time.time())
    while True:
        #chest info 红包信息
        #chestinfo = chest_info(httpRequest(opener, YTURLBASESSL + "index.php?s=/Chest/index/"))
            
        #Invest list info 投资列表
        """
        1： 企业标
        5: 秒标
        6: 净值标
        7：股权标
        9：创业标
        """
        typeList = (1, 5, 9)
        investList = investListRequest(opener, typeList)
        if(len(investList) == 0):
            time.sleep(30)
            continue #can't find any wanted invest 
            
        #loan info 借款信息
        logging.info(len(investList))
        
        for ivst in investList:
            ibid = ivst['id']
           
            if(int(ivst['borrow_type']) == 5):
                loaninfo = welfare_info(httpRequest(opener, YTURLBASESSL + "Financial/welfare"))
		print loaninfo
                if(loaninfo['available_cash'] > 0):
                    salt = loaninfo['uniqKey']
		    ppay = encrypt("root@2014", salt)
		    print ppay
                    #buy 秒标
                    values = {
                        '__hash__': loaninfo['__hash__'],
                        'ibnum': loaninfo['borrowNum'],
                        'lunchId': '0',  #红包ID
                        'amount': '100',
                        'p_pay': ppay,
                        'user_id': '54808'
                    }
                    buyinfo = buyRequest(opener, values)
                    if('tnum' in buyinfo):
                        tender_info(opener, loaninfo['borrowNum'], buyinfo['tnum'])
                    
            else:
                #企业或创业标
                loaninfo = loan_info(httpRequest(opener, YTURLBASESSL + "Invest/ViewBorrow/ibid/" + ibid))
                #coupon info
                lunchid = "0"
                ammount = "1000"
                couponinfo = couponListRequest(opener, loaninfo['borrowNum'])
                if(len(couponinfo['data'])):
                    lunchid = couponinfo['data'][0]['id']
                    ammount = couponinfo['data'][0]['user_constraint']
                #buy
                values = {
                    '__hash__': loaninfo['__hash__'],
                    'ibnum': loaninfo['borrowNum'],
                    'lunchId': lunchid,  #红包ID
                    'amount': ammount,
                    'p_pay': 'root@2014',
                    'user_id': '54808'
                    }
                #buyinfo = buyRequest(opener, values)
                #tender_info(opener, loaninfo['borrowNum'], buyinfo['tnum'])
        logging.info(loaninfo['borrowNum'])
        time.sleep(10000)
                
    pass

def readCookies(name):
    cookies = [file for file in os.listdir(BASEDIR + 'cookies') if os.path.isfile(BASEDIR + 'cookies/' + file)]
    names = map(lambda x: x[0:-10],cookies)
    if name not in names:
        return 0
    
    cookie_file_name = name + 'Cookie.txt'
    cookie = BASEDIR + 'cookies/' + cookie_file_name
    if not os.path.exists(cookie):
        return 0
    
    cj = cookielib.MozillaCookieJar()
    cj.load(cookie)
    dumpCookies(cj)
    for ck in cj:
        ck.expires = int(time.time() + 30 * 24 * 3600)
    cj.save(cookie)
    
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), urllib2.HTTPRedirectHandler())
    urllib2.install_opener(opener)
    
    buy_func(opener)

    opener.close()
    return 1 
      

def money(string):
    import platform
    if platform.system() == 'Windows':
         locale.setlocale(locale.LC_ALL, 'chs')
    else:
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
    
    if(readCookies("richardxieq")==0):
        username = raw_input(u"用户名：")
        password = raw_input(u'密码：')
        if(len(password) > 0):
            login(username, password)
    
    pass

    
if __name__ == '__main__':
    main()

