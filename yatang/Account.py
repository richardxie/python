#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from urllib2 import HTTPCookieProcessor,Request,build_opener,install_opener, HTTPRedirectHandler
from urllib import urlencode
import lxml.html.soupparser as soupparser
from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
import yatang, utils

class Account: 
    def __init__(self, cookie= None, name = None, level = None, balance = None, available = None, income = None, collection= None, payment= None):
        self.cookie= cookie
        self.name = name
        self.level = level
        self.balance= balance
        self.available = available
        self.income = income
        self.collection = collection
        self.payment = payment
        if cookie is not None:
            self.opener = build_opener(HTTPCookieProcessor(self.cookie), HTTPRedirectHandler())
            install_opener(self.opener)
        
    @staticmethod
    def account_info(html):
        dom = soupparser.fromstring(html)
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
        account_info = Account(
                               name=user_name,
                               level=level,
                               balance =account_balance,
                               available = account_available,
                               income = account_income,
                               collection=account_collection,
                               payment = account_payment
                        )
        return account_info
    
    def accountRequest(self):
        return Account.account_info(utils.httpRequest(self.opener, yatang.YTURLBASESSL + "index.php?s=/Account/").read())
