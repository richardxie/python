#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import utils, yatang, logging, traceback

logger = logging.getLogger('app')

from Borrow import Borrow
class Welfare(Borrow): 
    def __init__(self,hash_value, ibid, borrowType, borrowNum, available_cash,zxtbe, zdtbe, remain_amount, can_tender, uniqKey):
        Borrow.__init__(self, ibid, borrowType, borrowNum)
        self.hash_value = hash_value
        self.available_cash = available_cash
        self.zdtbe = zdtbe #最多投标额
        self.zxtbe = zxtbe #最小投标额
        self.remain_amount=remain_amount #剩余金额
        self.can_tender = can_tender
        self.uniqKey = uniqKey
          
    def __repr__(self):
        return "<Welfare(ibid='%s', type='%s', number='%s', minAmount='%f', cash='%f', hash_value='%s', uniqkey='%s', can_tender='%s')>" % (
                self.ibid, self.borrowType, self.borrowNum, self.zxtbe, self.available_cash, self.hash_value, self.uniqKey, self.can_tender)
    
    @staticmethod
    def welfare_info(html):
        logger.debug("welfare_info parsing...")
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        try:
            ibid_element = dom.xpath('//*[@class="amountt_input"]')
            if ibid_element and len(ibid_element) > 0:
                ibid = ibid_element[0].attrib['dataid']

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
                cash = utils.money(cash_element[0].attrib["value"])
            
            zdtbe_element = dom.xpath('//*[@id="zdtbe_' + ibid + '"]')
            if zdtbe_element and len(zdtbe_element) > 0:
                zdtbe = utils.money(zdtbe_element[0].attrib["value"])
            else:
                zdtbe = -1

            zxtbe_element = dom.xpath('//*[@id="zxtbe_' + ibid + '"]')
            if zxtbe_element and len(zxtbe_element) > 0:
                zxtbe = utils.money(zxtbe_element[0].attrib["value"])
            else:
                zxtbe = 1
                
            hxjk_element = dom.xpath('//*[@id="hxjk_' + ibid + '"]')
            if hxjk_element and len(hxjk_element) > 0:
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
                zxtbe = zxtbe,
                remain_amount = hxjk,
                can_tender=can_tender,
                uniqKey=uniqKey
                )
        except Exception, e:
            print e
            traceback.print_exc() 
            logger.warn("oops, parse walfare html failed!")
        pass
    
    @staticmethod
    def walfareRequest(opener):
        resp = utils.httpRequest(opener, yatang.YTURLBASESSL + "/Financial/welfare")
        if resp.code == 200:
            return Welfare.welfare_info(resp)
    