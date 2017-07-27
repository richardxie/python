#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DECIMAL, Boolean, DateTime, func, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields, ValidationError, pre_load, post_load

import os, sys
sys.path.append(os.path.dirname(__file__))

##### MODELS #####
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
    available = Column(DECIMAL(8, 2))
    income = Column(DECIMAL(8, 2))
    collection= Column(DECIMAL(8, 2))
    payment= Column(DECIMAL(8, 2))
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
    amount = Column(DECIMAL(8, 2))
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
    maxAmount = Column(DECIMAL(8, 2))
    minAmount = Column(DECIMAL(8, 2))
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
    minAPR = Column(DECIMAL(8, 2))#Annual Percentage Rate
    enabled = Column(Boolean())

    def __repr__(self):
        return "<TenderRule(id='%s', borrowType='%s', term='%d', minAPR='%f' enabled='%d')>" % (
                self.id, self.borrowType, self.term, self.minAPR, self.enabled)

    def __json__(self):
        return ["id", "borrowType", "term", "minAPR","enabled"]
    pass

class LoanInfo(CommonColumn):
    # 表的名字:
    __tablename__ = 'loan' #借款

    # 表的结构:
    ibid = Column(String(64), primary_key=True, autoincrement=False)
    name = Column(String(50)) #名称
    uniqKey = Column(String(20))
    _hash = Column(String(100))
    amount = Column(DECIMAL(8, 2)) #融资金额
    minAmount = Column(DECIMAL(8, 2)) # 起投金额
    repayType = Column(String(20)) #还款方式
    term = Column(String(20)) #期限
    limit = Column(Integer(), default=1) #期数
    apr = Column(DECIMAL(8, 2))#年化利率
    repaymentAmount = Column(DECIMAL(8, 2)) #还款总额


    @staticmethod
    def fromLoan(loan):
        info = LoanInfo()
        info.ibid = loan.ibid
        info.uniqKey = loan.uniqKey
        info._hash = loan.__hash__
        info.name = loan.name
        info.minAmount = loan.minAmount
        info.term = loan.term
        info.apr = loan.apr
        info.repaymentAmount = loan.repaymentAmount
        info.repayType = loan.repayType
        return info

    def __repr__(self):
        return "<Financing(name='%s', repayType='%s', term='%s', apr='%f', amount='%f', repaymentAmount='%f')>" % (
                self.name, self.repayType, self.term, self.apr, self.amount, self.repaymentAmount)

    def __json__(self):
        return ["id", "name","repayType", "term", "apr","amount","repaymentAmount"]
    pass

class FinancingInfo(CommonColumn):
    # 表的名字:
    __tablename__ = 'financing' #融资

    # 表的结构:
    id = Column(String(64), primary_key=True, autoincrement=False)
    name = Column(String(50)) #名称
    repaymentAmount = Column(DECIMAL(8, 2)) #还款总额
    datetime = Column(DateTime())
    recievedate = Column(String(20)) #应还日期
    status = Column(String(20)) #还款状态
    loan_id = Column(String(64), ForeignKey(LoanInfo.ibid))
    loan = relationship(LoanInfo)

    user_id = Column(String(64), ForeignKey(UserInfo.id))
    user = relationship(UserInfo)

    @staticmethod
    def fromFinancing(financing):
        info = FinancingInfo()
        import uuid
        info.id = str(uuid.uuid1())
        info.name = financing.name
        info.recievedate = financing.recievedate
        info.repaymentAmount = financing.repaymentAmount
        info.status = financing.status
        info.loan_id = financing.loan.ibid
        info.loan = LoanInfo.fromLoan(financing.loan)
        info.user_id = financing.userId
        return info

    def __repr__(self):
        return "<FinancingInfo(标题='%s', 还款总额='%.2f', 状态='%s')>" % (
                self.name, self.repaymentAmount, self.status)
     
    def __json__(self):
        return ["id", "name","datetime", "user_id", "loan_id","recievedate","repaymentAmount", "status", "loan"]

##### SCHEMAS #####
class LoanSchema(Schema):
    ibid = fields.Str(dump_only=True)
    name = fields.Str()
    term = fields.Str()
    apr  = fields.Decimal()

    @post_load
    def make_loan(self, data):
        from yt.Loan import Loan
        return Loan(**data)

class FinancingSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    recievedate = fields.Str()
    repaymentAmount  = fields.Decimal()
    loan = fields.Nested(LoanSchema)