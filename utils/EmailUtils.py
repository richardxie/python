#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from email.mime.text import  MIMEText
from email.header import Header
from smtplib import  SMTP_SSL

class EmailUtils: 
    def __init__(self):
        pass
    
          
    def send(self, mail_list):
        print "i'm sending email."
        #send email
        mail_host = 'smtp.163.com'
        mail_port = 465
        mail_user = 'test_shanlin@163.com'
        mail_pwd = '111111a'
        mail_receiver = ['13524470327@139.com','richard_xieq@foxmail.com']
        mail_to =','.join(mail_receiver)
        message ='<h3>本次雅堂签到的相关信息</h3>'
        message += '<ul>'
        for value in mail_list:
            msg = '<li>%s:v%s雅堂签到：%s</li>'%(value['user'].name, value['user'].level, value['data']['data']['tomorrow'])
            message += msg;
        message += '</ul>'
        msg = MIMEText(message,  _subtype='html', _charset='utf-8');
        msg['to'] = mail_to;
        msg['from'] = mail_user;
        msg['Subject'] = Header(u'雅堂签到', 'UTF-8').encode()
        server = SMTP_SSL(mail_host, mail_port)
        server.set_debuglevel(1)
        server.login(mail_user, mail_pwd)
        server.sendmail(mail_user, mail_to, msg.as_string())
        server.quit()
        pass

    def send_mail(self, data):
        #send email
        mail_host = 'smtp.163.com'
        mail_port = 465
        mail_user = 'test_shanlin@163.com'
        mail_pwd = '111111a'
        mail_receiver = ['13524470327@139.com','richard_xieq@foxmail.com']
        mail_to =','.join(mail_receiver)
        message ='<h3>本次投之家签到的相关信息</h3>'
        message += '<ul>'
        msg = '<li>%s投之家签到：%d</li>'%(data['info']['Username'], data['info']['Score'])
        message += msg;
        message += '</ul>'
        msg = MIMEText(message,  _subtype='html', _charset='utf-8');
        msg['to'] = mail_to;
        msg['from'] = mail_user;
        msg['Subject'] = Header(u'投之家签到', 'UTF-8').encode()
        server = SMTP_SSL(mail_host, mail_port)
        server.set_debuglevel(1)
        server.login(mail_user, mail_pwd)
        server.sendmail(mail_user, mail_to, msg.as_string())
        server.quit()
    