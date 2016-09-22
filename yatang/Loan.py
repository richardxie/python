#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

import lxml.html.soupparser as soupparser
from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import utils, yatang

from Borrow import Borrow
class Loan(Borrow): 
    def __init__(self, hash, ibid, bt, bn, cash, minAmount, uniqKey):
        print Borrow.__module__
        print Borrow.__class__
        Borrow.__init__(self, ibid, bt, bn)
        self.__hash__ = hash
        self.available_cash = cash
        self.minAmount = minAmount
        self.uniqKey = uniqKey
          
    
    @staticmethod
    def loan_info(html):
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        
        ibid_element = dom.xpath('//*[@id="ibid"]')
        ibid = ibid_element[0].attrib['value']
        borrowNum_element = dom.xpath("//*[@id=\"iborrownumid\"]")
        borrowNum = borrowNum_element[0].attrib['value']
        borrowType_element = dom.xpath('//*[@id="iborrowtype"]')
        borrowType = borrowType_element[0].attrib['value']
        hash_element = dom.xpath("/html/body/div[2]/div[3]/form/input")
        hash = hash_element[0].attrib["value"]
    
        uniqkey_element = dom.xpath("//*[@id='uniqKey']")
        uniqKey = uniqkey_element[0].attrib['value']
        
        # kyye
        cash_element = dom.xpath('//*[@id="zhkyye"]')
        cash = utils.money(cash_element[0].attrib['value'])
        
        # 最低投资金额
        minAmount_elemetn = dom.xpath('//*[@id="zxtbe"]')
        minAmount = utils.money(minAmount_elemetn[0].attrib['value'])
        
        return Loan(
            hash=hash,
            ibid=ibid,
            bt=borrowType,
            bn=borrowNum,
            cash=cash,
            minAmount=minAmount,
            uniqKey=uniqKey
            )
    
    @staticmethod
    def loanRequest(opener, ibid):
        return Loan.loan_info(utils.httpRequest(opener, yatang.YTURLBASESSL + "Invest/ViewBorrow/ibid/" + ibid))
    
