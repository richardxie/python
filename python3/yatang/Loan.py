#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import os, sys, logging, traceback

pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

import yatang
from utils import money, httpRequest
from Cookies import Cookies

logger = logging.getLogger("app")

from Borrow import Borrow
class Loan(Borrow): 
    def __init__(self, __hash__, ibid, bt, bn, name, cash, minAmount, uniqKey, uid, term, apr, repayType,repaymentAmount):
        Borrow.__init__(self, ibid, bt, bn)
        self.name = name
        self.__hash__ = __hash__
        self.available_cash = cash
        self.minAmount = minAmount
        self.uniqKey = uniqKey
        self.uid = uid
        self.term = term
        self.apr = apr
        self.repaymentAmount=repaymentAmount
        self.repayType = repayType
          
    def __repr__(self):
        return "<Loan(ibid='%s', borrowType='%s', borrowNum='%s', 期限 = '%s', 还款方式='%s', 还款总额='%s', 年利率='%.2f')>" % (
                self.ibid, self.borrowType, self.borrowNum, self.term, self.repayType, self.repaymentAmount, self.apr)

    @staticmethod
    def loan_info(html, info = None):
        logger.debug("借款信息解析")
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        try:
            name_element = dom.xpath("//head/title")
            if name_element and len(name_element) > 0:
                name = name_element[0].xpath('string()')[5:]
            else:
                name = "UNKNOWN"
            ibid_element = dom.xpath('//*[@id="ibid"]')
            if ibid_element and len(ibid_element) > 0:
                ibid = ibid_element[0].attrib['value']
            else:
                ibid = ''
            borrowNum_element = dom.xpath("//*[@id=\"iborrownumid\"]")
            if borrowNum_element and len(borrowNum_element) > 0:
                borrowNum = borrowNum_element[0].attrib['value']
            else:
                borrowNum=''
            borrowType_element = dom.xpath('//*[@id="iborrowtype"]')
            if borrowType_element and len(borrowType_element) > 0:
                borrowType = yatang.borrowTypeName(borrowType_element[0].attrib['value'])
            else:
                borrowType=''
            hash_element = dom.xpath("//input[@type='hidden' and @name='__hash__']/@value")
            if hash_element and len(hash_element) > 0:
                hash_value = str(hash_element[0])
            else: 
                hash_value = ''
                
            uniqkey_element = dom.xpath("//*[@id='uniqKey']")
            if uniqkey_element and len(uniqkey_element) > 0:
                uniqKey = uniqkey_element[0].attrib['value']
            else:
                uniqKey = ''
            
            # kyye
            cash_element = dom.xpath('//*[@id="zhkyye"]')
            if cash_element and len(cash_element) > 0:
                cash = money(cash_element[0].attrib['value'])
            else:
                cash = 0

            #user id
            uid_element = dom.xpath('//*[@id="cuid"]')
            if uid_element and len(uid_element) > 0:
                uid = uid_element[0].attrib['value']
            else:
                uid =''

            # 最低投资金额
            minAmount_element = dom.xpath('//*[@id="zxtbe"]')
            if minAmount_element and len(minAmount_element) > 0:
                minAmount = money(minAmount_element[0].attrib['value'])
            else:
                minAmount = 0

            apr_element = dom.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/span')
            if apr_element and len(apr_element) > 0:
                apr_str = apr_element[0].text.strip()
                apr = money(apr_str[:-1])
            else:
                print("apr unknown")
                apr = 0

            repayType_element = dom.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/div[3]/div[2]/span')
            if repayType_element and len(repayType_element) > 0:
                repayType = repayType_element[0].text
            else:
                repayType = '按月分期'

            repayAmount_element = dom.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[3]/div[1]/div[2]/div[2]')
            if repayAmount_element and len(repayAmount_element) > 0:
                repayAmount = money(repayAmount_element[0].text)
            else:
                repayAmount = 0

            term_element = dom.xpath('/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]')
            if term_element and len(term_element) > 0:
                term = term_element[0].text
            else:
                term = '1个月'

            return Loan(
                name = name,
                __hash__=hash_value,
                ibid=ibid,
                bt=borrowType,
                bn=borrowNum,
                cash=cash,
                minAmount=minAmount,
                uniqKey=uniqKey,
                uid = uid,
                term = term,
                apr = apr,
                repaymentAmount = repayAmount,
                repayType = repayType
                )
        except:
            logger.warn("oops, parse Loan html failed!")
            traceback.print_exc()

    
    @staticmethod
    def loanRequest(opener, info):
        url =''
        if 'id' in info:
            url = yatang.YTURLBASESSL + "/Invest/ViewBorrow/ibid/" + info['id']
        elif 'path' in info:
            url = yatang.YTURLBASESSL + info['path']
        print (url)
        response = httpRequest(opener, url)
        if response and response.code == 200:
            return Loan.loan_info(response, info)
        else:
            return None
    

if __name__ == '__main__':
    from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler
    c = Cookies()
    cj = c.readCookie('richardxieq')
    c.dumpCookies(cj)
    opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
    install_opener(opener)
    print(Loan.loanRequest(opener, {"id":"1087550"}));
    pass