#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import utils, yatang, logging

logger = logging.getLogger('app')

from Borrow import Borrow
class Welfare(Borrow): 
    def __init__(self,hash_value, ibid, borrowType, borrowNum, available_cash,zdtbe, remain_amount, can_tender, uniqKey):
        Borrow.__init__(self, ibid, borrowType, borrowNum)
        self.hash_value = hash_value
        self.available_cash = available_cash
        self.zdtbe = zdtbe #最多投标额
        self.remain_amount=remain_amount #剩余金额
        self.can_tender = can_tender
        self.uniqKey = uniqKey
          
    
    @staticmethod
    def welfare_info(html):
        logger.debug("welfare_info parsing...")
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
            
            zdtbe_element = dom.xpath('//*[@id="zdtbe_' + ibid + '"]')
            if zdtbe_element:
                zdtbe = utils.money(zdtbe_element[0].attrib["value"])
            else:
                zdtbe = -1
                
            hxjk_element = dom.xpath('//*[@id="hxjk_' + ibid + '"]')
            hxjk =  utils.money(hxjk_element[0].attrib["value"])
            
            can_tender = False
            incheck_element = dom.xpath('//*[@id="incheck_'+ ibid + '"]')
            if incheck_element:
                can_tender = True
            return Welfare(
                hash_value = hash_value,
                ibid = ibid,
                borrowType=borrowType,
                borrowNum=borrowNum,
                available_cash = cash,
                zdtbe = zdtbe,
                remain_amount = hxjk,
                can_tender=can_tender,
                uniqKey=uniqKey
                )
        except Exception, e:
            print e
            logger.warn("oops, parse walfare html failed!")
        pass
    
    @staticmethod
    def walfareRequest(opener):
        resp = utils.httpRequest(opener, yatang.YTURLBASESSL + "Financial/welfare")
        if resp.code == 200:
            return Welfare.welfare_info(resp)
    