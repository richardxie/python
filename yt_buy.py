#!/usr/bin/python2.7
#！-*- coding: utf-8 -*-

DEBUG = True
USECOOKIES = False
YTURLBASE = "http://jr.yatang.cn/"
YTURLBASESSL = "https://jr.yatang.cn/"
YT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0'
#BASEDIR = '/Users/wuqh/'
BASEDIR='./'
import urllib, http.cookiejar,json,time
import smtplib
import lxml.html.soupparser as soupparser
from lxml.html import html5parser
from lxml.html import html5parser
from html5lib import HTMLParser,treebuilders
from email.mime.text import  MIMEText
from email.header import Header
import os, locale, sys

def initSys():
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    pass
    
def dumpCookies(cj):
    for ck in cj:
        print (ck.name + ":" + ck.value)
    pass

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

def loan_info(html): 
    parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
    dom = html5parser.parse(html, parser = parser)
    
    ibid_element = dom.xpath('//*[@id="ibid"]')
    ibid = ibid_element[0].attrib['value']
    borrowNum_element = dom.xpath("//*[@id=\"iborrownumid\"]")
    borrowNum = borrowNum_element[0].attrib['value']
    
    hash_element = dom.xpath("/html/body/div[3]/form/input")
    hash =  hash_element[0].attrib["value"]
    return {
        "__hash__":hash,
        "ibid":ibid,
        "borrowNum":borrowNum
        }

def dumpInvestList(jsonresp):
    if(jsonresp['status'] == 1):
        if(int(jsonresp['data']['Total']) > 0):
            list = jsonresp['data']['Rows']
            for loan in list:
                print (loan['borrow_type'])
                print (loan['id'])
                print (loan['name'])
    pass

def investListRequest(opener, typeList):
    values = {
        'mode':1,
        'tpage[page]':1,
        'tpage[size]':20
    }
    data = urllib.parse.urlencode(values)
    headers = {
        'User-Agent': YT_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    req = urllib.request.Request(YTURLBASE + 'index.php?s=/Invest/GetBorrowlist', data.encode(encoding='UTF8'), headers)
    response = opener.open(req)

    jsonresp = json.loads(response.read().decode())
    dumpInvestList(jsonresp)
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
    data = urllib.parse.urlencode(values)
    headers = {
        'User-Agent': YT_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    req = urllib.request.Request(YTURLBASE + 'Ajax/getUserCoupon', data.encode(encoding='UTF8'), headers)
    response = opener.open(req)

    jsonresp = json.loads(response.read().decode())
    dumpCouponList(jsonresp)
    return jsonresp
    pass
 
def buyRequest(opener, values):
    #url: http://jr.yatang.cn/Invest/checkppay
    #post data
    """
    __hash__    
        3565f0b74518e8b60f5256e68575142f_d412a65b4b1c0ecdabca7d1192e99c93
        4e630c2cdc2070fb29a0dce7bbf7a85a
    amount    
        1520
    ibnum    
        1214QXR5601377
    lunchId    
        5128529
    p_pay    
        root@2014
    user_id    
        54808
    """
    
    data = urllib.parse.urlencode(values)
    headers = {
        'User-Agent': YT_USER_AGENT,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    req = urllib.request.Request(YTURLBASE + 'Invest/checkppay', data.encode(encoding='UTF8'), headers)
    response = opener.open(req)
    jsonresp = json.loads(response.read().decode())
    print(jsonresp)
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
    request = urllib.request.Request(url)
    response = opener.open(request)
    
    return response

def readCookies(name):
    cookies = [file for file in os.listdir(BASEDIR + 'cookies') if os.path.isfile(BASEDIR + 'cookies/' + file)]
    names = map(lambda x: x[0:-10],cookies)
    if name not in names:
        return 0
    
    cookie_file_name = name + 'Cookie.txt'
    cookie = BASEDIR + 'cookies/' + cookie_file_name
    if not os.path.exists(cookie):
        return 0
    
    cj = http.cookiejar.MozillaCookieJar()
    cj.load(cookie)
    dumpCookies(cj)
    for ck in cj:
        ck.expires = int(time.time() + 30 * 24 * 3600)
    cj.save(cookie)
    
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)
    
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
        return #can't find any wanted invest 
        
     #loan info 借款信息
    ibid = investList[0]['id']
    loaninfo = loan_info(httpRequest(opener, YTURLBASESSL + "Invest/ViewBorrow/ibid/" + ibid))
    print(loaninfo['borrowNum'])
    
    #coupon info
    couponinfo = couponListRequest(opener, loaninfo['borrowNum'])
    #couponinfo = couponListRequest(opener, '1215DREVK0160')
    
    #buy
    """
    __hash__    
        3565f0b74518e8b60f5256e68575142f_d412a65b4b1c0ecdabca7d1192e99c93
        4e630c2cdc2070fb29a0dce7bbf7a85a
    amount    
        1520
    ibnum    
        1214QXR5601377
    lunchId    
        5128529
    p_pay    
        root@2014
    user_id    
        54808
    """
    values = {
        '__hash__': loaninfo['__hash__'],
        'ibnum': loaninfo['borrowNum'],
        'lunchId': '0',
        'amount': '100',
        'p_pay': 'root@2014',
        'user_id': '54808'
        }
    buyinfo = buyRequest(opener, values)
    

    opener.close()
    return 1 
      

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
    
    if(readCookies("richardxieq")==0):
        username = raw_input(u"用户名：")
        password = raw_input(u'密码：')
        if(len(password) > 0):
            login(username, password)
    pass

def timer_sart():
    t = threading.Timer(5.0, buy_func)
    t.start()
    pass
    
def buy_func():
    print("buy function", time.time())
    timer_sart()
    pass
    
if __name__ == '__main__':
    main()

