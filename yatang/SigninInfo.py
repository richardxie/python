#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, DECIMAL
from yatang import Base


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