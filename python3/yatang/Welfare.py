#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
#秒标
from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import os, sys, re
from datetime import datetime
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

from utils import httpRequest, money
import yatang, logging, traceback

logger = logging.getLogger('app')

from Borrow import Borrow
class Welfare(Borrow): 
    def __init__(self,hash_value, ibid, borrowType, borrowNum, available_cash,zxtbe, zdtbe, remain_amount, uniqKey, starttime):
        Borrow.__init__(self, ibid, borrowType, borrowNum)
        self.hash_value = hash_value
        self.available_cash = available_cash
        self.zdtbe = zdtbe #最多投标额
        self.zxtbe = zxtbe #最小投标额
        self.remain_amount=remain_amount #剩余金额
        self.uniqKey = uniqKey
        self.starttime = starttime #开始时间
          
    def __repr__(self):
        return "<Welfare(ibid='%s', type='%s', number='%s', minAmount='%f', cash='%f', hash_value='%s', uniqkey='%s', starttime='%s')>" % (
                self.ibid, self.borrowType, self.borrowNum, self.zxtbe, self.available_cash, self.hash_value, self.uniqKey, self.starttime)
    
    @staticmethod
    def welfare_info(html):
        logger.debug("开心利是信息解析中...")
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        try:
            ibid_element = dom.xpath('//*[@class="amountt_input"]')
            if ibid_element and len(ibid_element) > 0:
                ibid = ibid_element[0].attrib['dataid']
            else:
                logger.warn("oops, 无效的html格式!")
                return #无效的html格式

            borrowNum_element = dom.xpath("//*[@id=\"iborrownumid_" + ibid + "\"]")
            if borrowNum_element and len(borrowNum_element) > 0:
                borrowNum = borrowNum_element[0].attrib['value']

            borrowType_element = dom.xpath('//*[@id="iborrowtype_' + ibid + '"]')
            if borrowType_element and len(borrowType_element) > 0:
                borrowType = borrowType_element[0].attrib['value']

            hash_element = dom.xpath("//input[@type='hidden' and @name='__hash__']/@value")
            if hash_element and len(hash_element) > 0:
                hash_value = str(hash_element[0])
        
            uniqkey_element = dom.xpath("//*[@id='uniqKey']")
            if uniqkey_element and len(uniqkey_element) > 0:
                uniqKey = uniqkey_element[0].attrib['value']
        
            cash_element = dom.xpath('//*[@id="ktmje_' + ibid + '"]')
            if cash_element and len(cash_element) > 0:
                cash = money(cash_element[0].attrib["value"])
            
            zdtbe_element = dom.xpath('//*[@id="zdtbe_' + ibid + '"]')
            if zdtbe_element and len(zdtbe_element) > 0:
                val = zdtbe_element[0].attrib["value"]
                if val == '无限制':
                    zdtbe = 80000
                else:
                    zdtbe = money(val)
            else:
                zdtbe = -1

            zxtbe_element = dom.xpath('//*[@id="zxtbe_' + ibid + '"]')
            if zxtbe_element and len(zxtbe_element) > 0:
                zxtbe = money(zxtbe_element[0].attrib["value"])
            else:
                zxtbe = 1
                
            hxjk_element = dom.xpath('//*[@id="hxjk_' + ibid + '"]')
            if hxjk_element and len(hxjk_element) > 0:
                hxjk =  money(hxjk_element[0].attrib["value"])
            
            starttime_element = dom.xpath('//*[@id="wks_'+ ibid + '"]')
            if starttime_element and len(starttime_element) > 0:
                m = re.match('(\d{2})月(\d{2})日\s(\d{2}):(\d{2}):(\d{2})', starttime_element[0].text)
                starttime = datetime(datetime.now().year, int(m.group(1)), int(m.group(2)), int(m.group(3)),  int(m.group(4)))
            else: 
                raise ValueError('开始时间未获取')

            incheck_element = dom.xpath('//*[@id="incheck2_'+ ibid + '"]')

            return Welfare(
                hash_value = hash_value,
                ibid = ibid,
                borrowType=borrowType,
                borrowNum=borrowNum,
                available_cash = cash,
                zdtbe = zdtbe,
                zxtbe = zxtbe,
                remain_amount = hxjk,
                uniqKey=uniqKey,
                starttime = starttime
                )
        except Exception as e:
            print (e)
            traceback.print_exc() 
            logger.warn("oops, 开心利是页面解析失败!")
        pass
    
    @staticmethod
    def walfareRequest(opener):
        resp = httpRequest(opener, yatang.YTURLBASESSL + "/Financial/welfare")
        if resp and resp.code == 200:
            return Welfare.welfare_info(resp)
    
if __name__ == '__main__':
    from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler, URLError, HTTPError
    from Cookies import Cookies
    c = Cookies()
    cj = c.readCookie('emmaye')
    #c.dumpCookies(cj)
    opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
    install_opener(opener)
    print(Welfare.walfareRequest(opener))