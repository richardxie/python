#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import utils, yatang

from Borrow import Borrow
class Loan(Borrow): 
    def __init__(self, __hash__, ibid, bt, bn, cash, minAmount, uniqKey, uid):
        Borrow.__init__(self, ibid, bt, bn)
        self.__hash__ = __hash__
        self.available_cash = cash
        self.minAmount = minAmount
        self.uniqKey = uniqKey
        self.uid = uid
          
    def __repr__(self):
        return "<Loan(ibid='%s', borrowType='%s', borrowNum='%s')>" % (
                self.ibid, self.borrowType, self.borrowNum)

    @staticmethod
    def loan_info(html):
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        try:
            ibid_element = dom.xpath('//*[@id="ibid"]')
            ibid = ibid_element[0].attrib['value']
            borrowNum_element = dom.xpath("//*[@id=\"iborrownumid\"]")
            borrowNum = borrowNum_element[0].attrib['value']
            borrowType_element = dom.xpath('//*[@id="iborrowtype"]')
            borrowType = borrowType_element[0].attrib['value']
            hash_element = dom.xpath("/html/body/div[2]/div[3]/form/input")
            hash_value = hash_element[0].attrib["value"]
        
            uniqkey_element = dom.xpath("//*[@id='uniqKey']")
            uniqKey = uniqkey_element[0].attrib['value']
            
            # kyye
            cash_element = dom.xpath('//*[@id="zhkyye"]')
            cash = utils.money(cash_element[0].attrib['value'])

            #user id
            uid_element = dom.xpath('//*[@id="cuid"]')
            uid = uid_element[0].attrib['value']

            # 最低投资金额
            minAmount_elemetn = dom.xpath('//*[@id="zxtbe"]')
            minAmount = utils.money(minAmount_elemetn[0].attrib['value'])
            
            return Loan(
                __hash__=hash_value,
                ibid=ibid,
                bt=borrowType,
                bn=borrowNum,
                cash=cash,
                minAmount=minAmount,
                uniqKey=uniqKey,
                uid = uid
                )
        except:
            logger.warn("oops, parse Loan html failed!")

    
    @staticmethod
    def loanRequest(opener, ibid):
        response = utils.httpRequest(opener, yatang.YTURLBASESSL + "Invest/ViewBorrow/ibid/" + ibid)
        if response.code == 200:
            return Loan.loan_info(response)
        else:
            return None
    
