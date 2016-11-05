#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 
from flask import Blueprint,request, Response, json, jsonify
from urllib2 import Request, install_opener,build_opener,HTTPCookieProcessor, HTTPRedirectHandler
from urllib import urlencode
from cookielib import MozillaCookieJar
from yatang import  Cookies, Financing
import logging, utils
from utils.json_encoder import new_object_encoder
utils.initSys()
logger = logging.getLogger("web")
web2 = Blueprint('web2', __name__)
@web2.route("/web2/")
def index():
    logger.info("web2 page!")
    data = {
        'page':'web2'
            }
    resp = Response(json.dumps(data), status=200, mimetype="application/json")
    return resp


@web2.route("/financing/")
def financing():
    logger.info('query financing for ')
    c = Cookies("./")
    cookie = c.readCookie("richardxieq")
    opener = build_opener(HTTPCookieProcessor(cookie))
    response = opener.open('https://jr.yatang.cn/Account/FinancingManagement/title/ReimbDetail')
    l = Financing.Financing.financing_info2(response, opener)
    jsonResp = json.dumps(l, cls=new_object_encoder(), check_circular=False, sort_keys=True)
    return Response(jsonResp, status=200, mimetype="application/json")
