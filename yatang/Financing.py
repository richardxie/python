#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import utils, yatang, logging, traceback
from yatang import YTURLBASESSL, Loan, Session
from modules import LoanInfo, FinancingInfo
from datetime import datetime
from utils.json_encoder import new_alchemy_encoder
import time, json
import pdb

logger = logging.getLogger('app')

class Financing(): 
    def __init__(self, name, date, repayment, status):
        self.name = name
        self.recievedate = date
        self.repaymentAmount = repayment
        self.status = status
          
    def __repr__(self):
        return "<Financing(项目标题='%s', 应还日期='%s', 还款总额='%f', 还款状态='%s', 年利率='%f')>" % (
                self.name, self.recievedate, self.repaymentAmount, self.status, self.loan.apr)

    @staticmethod
    def financing_info2(html, opener):
        logger.debug("融资信息解析")
        financing_list = []
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        financing_list = []
        try:
            financing_elements = dom.xpath('//tbody[@id="datalist"]')
            if financing_elements and len(financing_elements) > 0:
                for element in financing_elements[0].getchildren():
                    timestamp = datetime.fromtimestamp(float(element.attrib['date']))
                    date = element[0].text
                    peroid = element[2].text
                    name = element[3][0].text
                    ibid = element[3][0].attrib['href']
                    repaymentAmount = utils.money(element[4].text)
                    status = element[7].text.strip()
                    financing = Financing(name, date, repaymentAmount, status)
                    financing.loan = Loan.Loan.loanRequest(opener, {'path':ibid, 'time_limit':15})
                    time.sleep(0.5) #避免频繁请求，被流控
                    session = Session()
                    query = session.query(FinancingInfo).filter(FinancingInfo.name == name, FinancingInfo.status == status)
                    if query.count() == 0:
                        financing_info = FinancingInfo.fromFinancing(financing)
                        session.add(financing_info)
                        session.commit()
                    print financing
                    financing_list.append(financing)
        except Exception, e:
            print e
            traceback.print_exc() 
            logger.warn("oops, parse walfare html failed!")
        #update 已还
        names = map(lambda x: x.name, financing_list)

        session = Session()
        query = session.query(FinancingInfo).filter(~FinancingInfo.name.in_(names));
        print query.count()
        print json.dumps(query.all(), cls=new_alchemy_encoder(), check_circular=False, sort_keys=True)
        return financing_list

    @staticmethod
    def financing_info(html, opener):
        logger.debug("融资信息解析")
        financing_list = []
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        try:
            financing_elements = dom.xpath("/html/body/div[7]/div/div[2]/div[2]")
            
            if financing_elements and len(financing_elements) > 0:

                for element in financing_elements[0].findall('div'):
                    rows = element.findall('.//tr')
                    if rows:
                        name = rows[0].xpath('th')[0].xpath('string()').encode('utf-8')
                        ibid = rows[0].xpath('th')[0].xpath('a')[0].attrib['href']
                        amount = rows[1].xpath('td')[0].xpath('string()').encode('utf-8').replace("\t","").split("：")[1]
                        amount = utils.money(amount)
                        term =  rows[1].xpath('td')[1].xpath('string()').encode('utf-8').replace("\t","").split("：")[1].strip()
                        alreadypay =  rows[1].xpath('td')[2].xpath('string()').encode('utf-8')
                        apr =  rows[2].xpath('td')[0].xpath('string()').encode('utf-8').split("：")[1]
                        idx = apr.find("%")
                        if idx != -1:
                            apr = apr[0:idx]
                        repaytype = rows[2].xpath('td')[1].xpath('string()').encode('utf-8').replace("\t","").split("：")[1]
                        replayAmount =  rows[2].xpath('td')[2].xpath('string()').encode('utf-8').split("：")[1]
                        replayAmount =  utils.money(replayAmount)
                        info = Loan.Loan.loanRequest(opener, {'path':ibid, 'time_limit':15})
                        financing_list.append(info)

        except Exception, e:
            print e
            traceback.print_exc() 
            logger.warn("oops, parse walfare html failed!")
        return financing_list
    
    @staticmethod
    def financingRequest(opener):
        resp = utils.httpRequest(opener, yatang.YTURLBASESSL + "/Account/FinancingManagement/title/RepayFina")
        if resp.code == 200:
            return Financing.financing_info(resp, opener)
    