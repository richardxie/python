#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from urllib2 import HTTPCookieProcessor,Request,build_opener,install_opener, HTTPRedirectHandler
from urllib import urlencode
import lxml.html.soupparser as soupparser
from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import yatang, utils, logging
from modules import AccountInfo

logger = logging.getLogger("app")

class Account: 
    def __init__(self, cookie= None, account_info = None):
        self.cookie= cookie
        self.account_info = account_info
        if cookie is not None:
            self.opener = build_opener(HTTPCookieProcessor(self.cookie), HTTPRedirectHandler())
            install_opener(self.opener)
        
    @staticmethod
    def account_info(html):
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        try:
            user_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/div[1]/div[1]/p[2]/b')
            user_name = user_ele[0].text
            balance_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/ul[1]/li[1]/p/span')
            account_balance = utils.money(balance_ele[0].text)
            
            availabe_ele = dom.xpath("/html/body/div[7]/div/div/div[1]/ul[1]/li[2]/p/span")
            account_available = utils.money(availabe_ele[0].text)
            
            income_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/ul[1]/li[3]/p/span')
            account_income = utils.money(income_ele[0].text)
            collection_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/ul[1]/li[4]/p/span')
            account_collection = utils.money(collection_ele[0].text)
            payment_ele = dom.xpath('/html/body/div[7]/div/div/div[1]/ul[2]/li[4]/p/span')
            account_payment = utils.money(payment_ele[0].text)
            level_ele = dom.xpath("/html/body/div[7]/div/div/div[1]/div[1]/div[1]/p[2]/a/img")
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

            return account_info
        except Exception,e:
            print(e)
            logger.warn("oops, parse Account html failed!")
            return None

    
    def accountRequest(self):
        response = utils.httpRequest(self.opener, yatang.YTURLBASESSL + "index.php?s=/Account/")
        if response.code == 200 :
            return Account.account_info(response)

