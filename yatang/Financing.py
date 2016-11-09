#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
from urllib2 import install_opener,build_opener,HTTPCookieProcessor
import utils, yatang, logging, traceback
from yatang import YTURLBASESSL, Loan, Session
from modules import LoanInfo, FinancingInfo
from datetime import datetime
from utils.json_encoder import new_alchemy_encoder
import time, json
import pdb

logger = logging.getLogger('app')

class Financing(): 
    def __init__(self, name, cookie=None, date = None, repayment = None, status = None):
        self.name = name
        self.recievedate = date
        self.repaymentAmount = repayment
        self.status = status
        self.cookie = cookie
        if cookie:
            self.opener = build_opener(HTTPCookieProcessor(self.cookie))
            install_opener(self.opener)
          
    def __repr__(self):
        return "<Financing(项目标题='%s', 应还日期='%s', 还款总额='%f', 还款状态='%s', 年利率='%f')>" % (
                self.name, self.recievedate, self.repaymentAmount, self.status, self.loan.apr)

    def financing_info2(self, html):
        logger.debug("融资信息解析")
        financing_list = []
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        financing_list = []
        last = True
        next_page_url = ''
        try:
            next_page_element = dom.xpath("/html/body/div[7]/div/div[2]/div[2]/div/div/a[1]")
            if next_page_element and len(next_page_element) > 0:
                last  = False;
                next_page_url = next_page_element[0].attrib['href']
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
                    financing = Financing(name = name, date=date, repayment=repaymentAmount, status=status)
                    financing.loan = Loan.Loan.loanRequest(self.opener, {'path':ibid, 'time_limit':15})
                    time.sleep(0.2) #避免频繁请求，被流控
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
            logger.warn("oops, parse financing html failed!")
        return {
                "last":last,
                "next_page_url":next_page_url,
                "data":financing_list
                }

    def financingRequestPagable(self):
        financing_list = []
        data = self.financingRequest({'page':'1'})
        financing_list.extend(data['data'])
        if not data['last']:
            data = self.financingRequest(data)
            financing_list.extend(data['data'])
        return financing_list

    def financingRequest(self, info):
        url = ''
        if 'page' in info:
            url = yatang.YTURLBASESSL + "/Account/FinancingManagement/title/ReimbDetail?p=" + info['page']
        elif 'next_page_url' in info:
            url = yatang.YTURLBASESSL + info['next_page_url']
        print url
        resp = utils.httpRequest(self.opener, url)
        if resp.code == 200:
            return self.financing_info2(resp)
    