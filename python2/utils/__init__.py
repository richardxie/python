#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from EmailUtils import EmailUtils
from urllib2 import Request, URLError, HTTPError
from PyV8 import JSContext
import logging, logging.config, threading
from random import randint
import yaml, sys, os, socket

Salt = '1234qwer'

def initSys():
    # UTF-8
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    # logging
    with open("logging-conf.yaml") as f:
        D = yaml.load(f)
        logging.config.dictConfig(D)

    #System path
    sys.path.append(os.path.dirname(__file__))
    pythonpath = os.getenv('PYTHONPATH')
    if pythonpath is not None:
        paths = pythonpath.split(':' if os.name=='posix' else ';')
        for path in paths:
            if not path in sys.path:
                sys.path.append(path)

    #socket timeout
    socket.setdefaulttimeout(30.0) 

    pass

def httpRequest(opener, url):
    request = Request(url)
    try:
        response = opener.open(request, timeout=20)
        return response
    except URLError, e:
        print e
        logging.getLogger("app").warn(e)
    except HTTPError as h:
        print h
        logging.getLogger("app").warn(h)
    except socket.timeout as t:
         logging.getLogger("app").warn(t)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        logging.getLogger("app").warn('Unexpected error:',  sys.exc_info()[0])
   

def encryptPassword(password, verifycode):
    with JSContext() as jsctx:
        with open("encrypt.js") as jsfile:
            jsctx.eval(jsfile.read())
            encryptFunc = jsctx.locals.encrypt;
            pwd = encryptFunc(password, verifycode)
    return pwd

def encryptTradePassword(tradepassword, uniqkey, task = None):
    print threading.current_thread().name
    if threading.current_thread().name == "MainThread":
        with JSContext() as jsctx:
            with open("encrypt.js") as jsfile:
                jsctx.eval(jsfile.read())
                encryptFunc = jsctx.locals.encrypt2;
                pwd = encryptFunc(tradepassword, uniqkey)
    else:
        if task:
            data = {
                    "type":"encrypt2",
                    "data": {"pwd":tradepassword, "key":uniqkey},
                    "collaborative_id": randint(1,100),
                    "queue":task.q
                    }
            task.mainQueue.put(data)
            resp = task.q.get()
            pwd = resp['data']
    return pwd

def money(string):
    import platform, locale
    if platform.system() == 'Windows':
        locale.setlocale(locale.LC_ALL, 'chs')
    else:
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    sym = locale.localeconv()['currency_symbol']
    if sym:
        string = string.replace(sym, '')
    ts = locale.localeconv()['thousands_sep']
    if ts:
        string = string.replace(ts, '')  # next, replace the decimal point with a 
    dd = locale.localeconv()['decimal_point']
    if dd:
        string = string.replace(dd, '.')  # finally, parse the string
    return float(string)   