#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 

from email.mime.text import  MIMEText
from email.header import Header
from smtplib import  SMTP_SSL
import logging

logger = logging.getLogger("app")
class email_utils: 
    
    def __init__(self):
        pass
          
    def send(self, mail_list):
        if len(mail_list) ==0:
            return
        
        logger.info("email sending")
        #send email
        mail_host = 'smtp.163.com'
        mail_port = 465
        mail_user = 'test_shanlin@163.com'
        mail_pwd = '111111a'
        mail_receiver = ['13524470327@139.com','richard.xieq@foxmail.com']
        mail_to =','.join(mail_receiver)
        message ='<h3>本次雅堂签到的相关信息</h3>'
        message += '<ul>'
        for value in mail_list:
            msg = '<li>%s:v%s雅堂签到：%s</li>'%(value['user'].name, value['user'].level, value['data']['data']['tomorrow'])
            message += msg;
        message += '</ul>'
        logger.info('email content:' + message)
        msg = MIMEText(message,  _subtype='html', _charset='utf-8');
        msg['to'] = mail_to;
        msg['from'] = mail_user;
        msg['Subject'] = Header(u'雅堂签到', 'UTF-8').encode()
        try:
            server = SMTP_SSL(mail_host, mail_port)
            #server.set_debuglevel(1)
            server.login(mail_user, mail_pwd)
            server.sendmail(mail_user, mail_to, msg.as_string())
            server.quit()
        except Exception as e:
            print(e)
            logger.warn("sendmail error.")
        pass

    def message(self, data):
        message ='<h3>本次投之家签到的相关信息</h3>'
        message += '<ul>'
        msg = '<li>投之家签到：%d</li>'%(data['todayScore'])
        message += msg;
        message += '</ul>'
        logger.info('email content:' + message)
        return message

    def send_mail(self, data):
        #send email
        mail_host = 'smtp.163.com'
        mail_port = 465
        mail_user = 'test_shanlin@163.com'
        mail_pwd = '111111a'
        mail_receiver = ['13524470327@139.com','richard.xieq@foxmail.com']
        mail_to =','.join(mail_receiver)
        message = self.message(data)
        msg = MIMEText(message,  _subtype='html', _charset='utf-8');
        msg['to'] = mail_to;
        msg['from'] = mail_user;
        msg['Subject'] = Header(u'投之家签到', 'UTF-8').encode()
        try:
            server = SMTP_SSL(mail_host, mail_port)
            #server.set_debuglevel(1)
            server.login(mail_user, mail_pwd)
            server.sendmail(mail_user, mail_to, msg.as_string())
            server.quit()
        except Exception as e:
            print(e)
            logger.warn("sendmail error.")
    
if __name__ == '__main__':
    data = {"todayScore": 1}
    sender = email_utils(); 
    sender.send_mail(data)