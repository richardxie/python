#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from logging import config
from yaml import load
from os import path
db_config = {
    "mysql" : {
        'host':'192.16.3.239',
        'port':'3306',
        'user':'admin',
        'instancename':'test',
        'password':'admin'
    },
    "sqlite3" : {
        'host':'',
        'dbname':'/usr/src/vagrant/test.db'
    }
}

auto_tender_names = ['richardxieq','emmaye']

def initConfig():
    # logging
    p = path.dirname(path.abspath(__file__))
    with open(p + "/logging-conf.yaml") as f:
        D = load(f)
        config.dictConfig(D)
    pass
