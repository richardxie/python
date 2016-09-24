#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DECIMAL

Base = declarative_base()

class User(Base):
	 # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement = True)
    user_id = Column(String(32))
    name = Column(String(32))
    pass

    def __repr__(self):
        return "<User(user_id='%s', name='%s')>" % (
                self.user_id, self.name)
	pass

class AccountInfo(Base):
     # 表的名字:
    __tablename__ = 'account'

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement = True)
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

class SigninInfo(Base):
     # 表的名字:
    __tablename__ = 'signin'

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement = True)
    name = Column(String(20))
    signin_date = Column(String(10))
    prev_signin_data = Column(String(10))
    pass

    def __repr__(self):
        return "<Signin(name='%s', data='%s', previous_data='%s')>" % (
                self.name, self.signin_date, self.prev_signin_data)

class InvestInfo(Base):
     # 表的名字:
    __tablename__ = 'invest'

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement = True)
    name = Column(String(20))
    amount = Column(DECIMAL())
    date = Column(String(10))
    pass

    def __repr__(self):
        return "<InvestInfo(name='%s', data='%s', amount='%s')>" % (
                self.name, self.date, self.amount)