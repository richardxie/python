#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 
from flask import Blueprint,request, Response, json, jsonify
from urllib2 import Request, install_opener,build_opener,HTTPCookieProcessor, HTTPRedirectHandler
from urllib import urlencode
from cookielib import MozillaCookieJar
from yatang import  Cookies, Financing, Session
from yatang.modules import FinancingInfo, UserInfo
import logging, utils
from utils.json_encoder import new_alchemy_encoder
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


@web2.route("/<user>/financing")
def financings(user):
    logger.info('query financing for %s'%(user))

    session = Session()

    query = session.query(UserInfo).filter(UserInfo.name == user, UserInfo.website == 'yt')
    if query.count() == 0:
        data = {
            'errorCode':'002',
            'errorMsg':'用户名不存在'
        }
        info = json.dumps(data)
    else:
        query = session.query(FinancingInfo).filter(FinancingInfo.status == '未还')
        if query.count() == 0:
            data = {
                'errorCode':'001',
                'errorMsg':'没有未还融资'
            }
            info = json.dumps(data)
        else:
            info = json.dumps(query.all(), cls=new_alchemy_encoder(), check_circular=False, sort_keys=True)
    resp = Response(info, status=200, mimetype="application/json")
    return resp

@web2.route("/<user>/financing/<title>")
def financing(user, title):
    logger.info('query financing( %s) for %s '%(title, user))

    session = Session()
    query = session.query(UserInfo).filter(UserInfo.name == user, UserInfo.website == 'yt')
    if query.count() == 0:
        data = {
            'errorCode':'002',
            'errorMsg':'用户名不存在'
        }
        info = json.dumps(data)
    else:
        query = session.query(FinancingInfo).filter(FinancingInfo.name == title, FinancingInfo.status == '未还')
        if query.count() == 0:
            data = {
                'errorCode':'001',
                'errorMsg':'没有未还融资'
            }
            info = json.dumps(data)
        else:
            info = json.dumps(query.one(), cls=new_alchemy_encoder(), check_circular=False, sort_keys=True)
    resp = Response(info, status=200, mimetype="application/json")
    return resp
