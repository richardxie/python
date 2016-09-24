#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DECIMAL
from yatang import Base


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