#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DECIMAL, Boolean, DateTime, func
from datetime import datetime

import os, sys
sys.path.append(os.path.dirname(__file__))

Base = declarative_base()
class CommonColumn(Base):
    __abstract__ = True
    create_date = Column(DateTime, default=func.now())
    update_date = Column(DateTime)
    version = Column(Integer, nullable=False)

    __mapper_args__ = {
        "version_id_col": version
    }
    pass

class UserInfo(CommonColumn):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement=False)
    website = Column(String(32), default="yt")
    user_id = Column(String(32), default="000")
    name = Column(String(32))
    password = Column(String(64))
    trade_password = Column(String(64), default="000")
    pass

    def __repr__(self):
        return "<User(user_id='%s', name='%s')>" % (
                self.user_id, self.name)

    def __json__(self):
        return ["id", "user_id", "name", "password"]

class AccountInfo(CommonColumn):
    # 表的名字:
    __tablename__ = 'account'

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement=False)
    name = Column(String(20))
    level = Column(String(10))
    balance = Column(DECIMAL())
    available = Column(DECIMAL())
    income = Column(DECIMAL())
    collection= Column(DECIMAL())
    payment= Column(DECIMAL())
    pass

    def __repr__(self):
        return "<Account(name='%s', balance='%s', income='%s')>" % (
                self.name, self.balance, self.income)

class SigninInfo(CommonColumn):
    # 表的名字:
    __tablename__ = 'signin'

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement=False)
    name = Column(String(20))
    website = Column(String(20))
    signin_date = Column(DateTime, default=func.now())
    prev_signin_date = Column(DateTime)
    pass

    def __repr__(self):
        return "<Signin(name='%s', web='%s', signin_date='%s', prev_signin_date='%s')>" % (
                self.name, self.website, str(self.signin_date), str(self.prev_signin_date))

class InvestInfo(CommonColumn):
    # 表的名字:
    __tablename__ = 'invest'

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement=False)
    name = Column(String(20))
    amount = Column(DECIMAL())
    date = Column(String(10))
    pass

    def __repr__(self):
        return "<InvestInfo(name='%s', data='%s', amount='%s')>" % (
                self.name, self.date, self.amount)

class WelfareInfo(CommonColumn):
    # 表的名字:
    __tablename__ = 'welfare'

    # 表的结构:
    ibid = Column(String(64), primary_key=True, autoincrement=False)
    borrowType = Column(String(20))
    borrowNum = Column(String(50))
    maxAmount = Column(DECIMAL())
    minAmount = Column(DECIMAL())
    pass

    @staticmethod
    def fromWelfare(welfare):
        info = WelfareInfo()
        info.ibid = welfare.ibid
        info.borrowNum = welfare.borrowNum
        info.borrowType = welfare.borrowType
        info.minAmount = welfare.zxtbe
        info.maxAmount = welfare.zdtbe
        return info

    def __repr__(self):
        return "<WelfareInfo(ibid='%s', type='%s', number='%s', minAmount='%f', maxAmount='%f')>" % (
                self.ibid, self.borrowType, self.borrowNum, self.minAmount, self.maxAmount)

class TenderRule(CommonColumn):
    # 表的名字:
    __tablename__ = 'tenderrules'

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement=False)
    borrowType = Column(String(20))
    term = Column(Integer())
    minAPR = Column(DECIMAL())#Annual Percentage Rate
    enabled = Column(Boolean())

    def __repr__(self):
        return "<TenderRule(id='%s', borrowType='%s', term='%d', minAPR='%f' enabled='%d')>" % (
                self.id, self.borrowType, self.term, self.minAPR, self.enabled)

    def __json__(self):
        return ["id", "borrowType", "term", "minAPR","enabled"]
    pass
