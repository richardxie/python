#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
from time import time, sleep
from datetime import datetime,timedelta
from argparse import ArgumentParser
from tender import Tender
from tenderWF import TenderWF
from tenderCF import TenderCF
import sys,logging,utils,conf
logger = logging.getLogger("app")

#python app.py -t crowdfunding  -v
if __name__ == '__main__':
   
    #初始化
    utils.initSys()
    conf.initConfig()
    parser = ArgumentParser()
    parser.add_argument('-t', '--type')
    parser.add_argument('-amt', '--amount')
    parser.add_argument('-u', '--user')
    parser.add_argument('-v', dest='verbose', action='store_true')
    args = parser.parse_args()
    try:
        {
            'welfare' : TenderWF().timming_exec,
            'asset' : Tender(args.user if args.user is not None else 'richardxieq').timming_exec,
            'crowdfunding' : TenderCF(args.user if args.user is not None else 'richardxieq', 
                                        args.amount if args.amount is not None else 15000)
                                        .crowdfunding_tender,
            'test' : lambda : logger.info("未实现")
        }[args.type]()
    except AttributeError as attrerr:
        logger.info('无效的任务名：%s' % args.type)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        print("finally")
    