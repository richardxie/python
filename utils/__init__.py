from EmailUtils import EmailUtils
from urllib2 import Request
import logging, logging.config
import yaml, sys, os

def initSys():
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    
    with open("logging-conf.yaml") as f:
        D = yaml.load(f)
        logging.config.dictConfig(D)

    sys.path.append(os.path.dirname(__file__))
    pythonpath = os.getenv('PYTHONPATH')
    if pythonpath is not None:
        paths = pythonpath.split(':' if os.name=='posix' else ';')
        for path in paths:
            if not path in sys.path:
                sys.path.append(path)
    pass

def httpRequest(opener, url):
    request = Request(url)
    response = opener.open(request)
    return response

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