#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
#众筹
from lxml.html import html5parser
from html5lib import HTMLParser, treebuilders
from datetime import datetime,timedelta
import os, sys
pythonpath = os.path.dirname(__file__)
pythonpath = os.path.abspath(os.path.join(pythonpath, os.pardir))
if pythonpath is not None:
    paths = pythonpath.split(':' if os.name=='posix' else ';')
    for path in paths:
        if not path in sys.path:
            sys.path.append(path)

from utils import httpRequest, money
import yatang, logging, traceback

logger = logging.getLogger('app')
class Crowdfunding: 
    def __init__(self,proj_id, hash_value='', qtje=1000, dzje=100000, xtje=1000, starttime = datetime.now(), uniqKey=''):
        self.project_id = proj_id
        self.hash_value = hash_value
        self.qtje = qtje #起投金额
        self.dzje = dzje #递增金额
        self.xtje = xtje #限投金额
        self.starttime = starttime #投标开始时间
        self.uniqKey = uniqKey
          
    def __repr__(self):
        return "<Crowdfunding(项目编号='%s',起投金额='%.2f',递增金额='%.2f',限投金额='%.2f',hash_value='%s', uniqkey='%s')>" % (
               self.project_id, self.qtje, self.dzje, self.xtje, self.hash_value, self.uniqKey)
    
    @staticmethod
    def crowdfunding_detail(html):
        logger.debug("众筹详细信息解析")
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        projectId_element = dom.xpath('//*[@id="projctid"]')
        if projectId_element and len(projectId_element) > 0:
            projId = projectId_element[0].attrib['value']
        else:
            projId = ''

        qtje_element = dom.xpath('//*[@id="qtje"]')
        if qtje_element and len(qtje_element) > 0:
            qtje = money(qtje_element[0].attrib['value'])
        else: 
            qtje = 0
        
        dzje_element = dom.xpath('//*[@id="dzje"]')
        if dzje_element and len(dzje_element) > 0:
            dzje = money(dzje_element[0].attrib['value'])
        else: 
            dzje = 0
        
        xtje_element = dom.xpath('//*[@id="xtje"]')
        if xtje_element and len(xtje_element) > 0:
            xtje = money(xtje_element[0].attrib['value'])
        else: 
            xtje = 0
        
        starttime_element = dom.xpath('//input[@id="preheat_left_time"]')
        if starttime_element and len(starttime_element) > 0:
            starttime = datetime.strptime( starttime_element[0].attrib['value'], "%Y-%m-%d %H:%M:%S")
        else: 
            starttime = datetime.now()

        hash_element = dom.xpath("//input[@type='hidden' and @name='__hash__']/@value")
        if hash_element and len(hash_element) > 0:
            hash_value = str(hash_element[0])
        else: 
            hash_value = ''
        
        uniqkey_element = dom.xpath("//*[@id='uniqKey']")
        if uniqkey_element and len(uniqkey_element) > 0:
            uniqKey = uniqkey_element[0].attrib['value']
        else:
            uniqKey = ''

        return Crowdfunding(
            proj_id = projId,
            qtje = qtje,
            dzje = dzje,
            xtje = xtje,
            hash_value = hash_value,
            uniqKey = uniqKey,
            starttime = starttime
        )
        pass

class Crowdfundings: 
    def __init__(self, opener):
        self.opener = opener
    
    def crowdfundingRequest(self):
        resp = httpRequest(self.opener, yatang.YTURLBASESSL + "/Crowdfunding")
        if resp and resp.code == 200:
            return self.crowdfundingDetailRequest(Crowdfundings.crowdfunding_info(resp))
    
    def crowdfundingDetailRequest(self, projectURL):
        resp = httpRequest(self.opener, yatang.YTURLBASESSL + projectURL)
        if resp and resp.code == 200:
            return Crowdfunding.crowdfunding_detail(resp)

    @staticmethod
    def crowdfunding_info(html):
        logger.debug("众筹信息解析中...")
        parser = HTMLParser(tree=treebuilders.getTreeBuilder('lxml') , namespaceHTMLElements=False)
        dom = html5parser.parse(html, parser=parser)
        projectURL_e = dom.xpath("////div[@class='zc_detail_box']/a")
        return projectURL_e[0].attrib['href']

    
