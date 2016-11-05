#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
db_config = {
    "mysql" : {
        'host':'10.10.32.51',
        'port':'3306',
        'user':'uNjZxSYgbXifmCHt',
        'instancename':'H6JqdLoA29ukwlEc',
        'password':'pCHpS0XA4V7JWhPFZ'
    },
    "mysql-dev" : {
        'host':'mysql',
        'port':'3306',
        'user':'root',
        'instancename':'mysqldb',
        'password':'admin123'
    },
    "sqlite3" : {
        'host':'',
        'dbname':'/usr/src/vagrant/test.db'
    },
    "sqlite3-dev" : {
        'host':'',
        'dbname':'test.db'
    }
}

auto_tender_names = ['richardxieq','emmaye']
