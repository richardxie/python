#!/usr/bin/python3.6
# ！-*- coding: utf-8 -*-
from urllib.request import Request, URLError, HTTPError
import sys, os, socket
sys.path.append(os.path.dirname(__file__))
from js_utils import Encryptor

def initSys():
    # UTF-8
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')

    #System path
    sys.path.append(os.path.dirname(__file__))
    #pythonpath = os.getenv('PYTHONPATH')
    pythonpath = "E:/SlProject/v2"
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
        response = opener.open(request, timeout=200)
        return response
    except URLError as e:
        print(e)
        logging.getLogger("app").warn(e)
    except HTTPError as h:
        print(h)
        logging.getLogger("app").warn(h)
    except socket.timeout as t:
         logging.getLogger("app").warn(t)
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        logging.getLogger("app").warn('Unexpected error:',  sys.exc_info()[0])

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