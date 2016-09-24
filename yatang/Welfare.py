#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import utils, yatang

from Borrow import Borrow
class Welfare(Borrow): 
    def __init__(self, __hash__, ibid, bt, bn, cash,uniqkey):
        Borrow.__init__(self, ibid, bt, bn)
        self.__hash__ = hash
        self.available_cash = cash
        self.uniqkey = uniqkey
          
    
    @staticmethod
    def welfare_info(html):
        print "welfare_info start."
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        try:
            ibid_element = dom.xpath('//*[@class="amountt_input"]')
            ibid = ibid_element[0].attrib['dataid']
            borrowNum_element = dom.xpath("//*[@id=\"iborrownumid_" + ibid + "\"]")
            borrowNum = borrowNum_element[0].attrib['value']
            borrowType_element = dom.xpath('//*[@id="iborrowtype_' + ibid + '"]')
            borrowType = borrowType_element[0].attrib['value']
            hash_element = dom.xpath("/html/body/div[3]/div[4]/div[2]/div[3]/form/input[2]")
            hash_value = hash_element[0].attrib["value"]
        
            uniqkey_element = dom.xpath("//*[@id='uniqKey']")
            uniqKey = uniqkey_element[0].attrib['value']
        
            cash_element = dom.xpath('//*[@id="ktmje_' + ibid + '"]')
            cash = utils.money(cash_element[0].attrib["value"])
            return Welfare(
                __hash__ = hash_value,
                ibid = ibid,
                borrowType=borrowType,
                borrowNum=borrowNum,
                available_cash = cash,
                uniqKey=uniqKey
                )
        except:
            logger.warn("oops, parse walfare html failed!")
        pass
    
    @staticmethod
    def walfareRequest(opener):
        return Welfare.walfarem_info(utils.httpRequest(opener, yatang.YTURLBASESSL + "Financial/welfare"))
    