#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

from urllib.request import HTTPCookieProcessor,build_opener,install_opener, HTTPRedirectHandler
from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import os, sys, logging

pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

from modules import AccountInfo
from Cookies import Cookies
from utils import httpRequest,money
import yatang

logger = logging.getLogger("app")

class Account: 
    def __init__(self, opener= None, account_info = None):
        self.account_info = account_info
        self.opener = opener
        
    @staticmethod
    def account_info(html):
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        try:
            user_ele = dom.xpath('/html/body/div[6]/div/div/div[1]/div[1]/div[1]/p[2]/b')
            user_name = user_ele[0].text
            balance_ele = dom.xpath('/html/body/div[6]/div/div/div[1]/ul[1]/li[1]/p/span')
            account_balance = money(balance_ele[0].text)
            
            availabe_ele = dom.xpath("/html/body/div[6]/div/div/div[1]/ul[1]/li[2]/p/span")
            account_available = money(availabe_ele[0].text)
            
            income_ele = dom.xpath('/html/body/div[6]/div/div/div[1]/ul[1]/li[3]/p/span')
            account_income =  money(income_ele[0].text)
            collection_ele = dom.xpath('/html/body/div[6]/div/div/div[1]/ul[1]/li[4]/p/span')
            account_collection = money(collection_ele[0].text)
            payment_ele = dom.xpath('/html/body/div[6]/div/div/div[1]/ul[2]/li[4]/p/span')
            account_payment =  money(payment_ele[0].text)
            level_ele = dom.xpath("/html/body/div[6]/div/div/div[1]/div[1]/div[1]/p[2]/a/img")
            level = level_ele[0].get("src").split("/")[-1].split(".")[0]
            import uuid
            account_info = AccountInfo(
                                id=str(uuid.uuid1()),                             
                                   name=user_name,
                                   level=level,
                                   balance =account_balance,
                                   available = account_available,
                                   income = account_income,
                                   collection=account_collection,
                                   payment = account_payment
                            )
            session = yatang.Session()
            query = session.query(AccountInfo).filter(AccountInfo.name == account_info.name)
            if(query.count() == 0):
                session.add(account_info)
                session.commit()

            return account_info
        except Exception as e:
            print(e)
            logger.warn("oops, parse Account html failed!")
            return None

    
    def accountRequest(self):
        with httpRequest(self.opener, yatang.YTURLBASESSL + "/Account/home") as response:
            if response and response.code == 200 :
                return Account.account_info(response)

if __name__ == '__main__':
    c = Cookies()
    cj = c.readCookie('richardxieq')
    #c.dumpCookies(cj)
    opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
    install_opener(opener)

    acc = Account(opener)
    print(acc.accountRequest())
    pass