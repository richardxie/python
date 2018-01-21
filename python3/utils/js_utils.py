#!/usr/bin/python3.6
# -*- coding: utf-8 -*- 
import execjs, threading, os
class Encryptor: 
    def __init__(self):
        pass

    def encrypt(self, password, timestamp):
        js_str = ''
        path = os.path.dirname(os.path.abspath(__file__))
        print(path)
        with open(path + '/aes.js') as f:
             for line in f:
                js_str = js_str + line

        default_exec = execjs.get()
        #print(js_str)
        ctx = default_exec.compile(js_str)
        pwd = ctx.call('ytUtil.encrypt',password, timestamp)
        return pwd

    def encryptPassword(self, password, verifycode):
        js_str = ''
        path = os.path.dirname(os.path.abspath(__file__))
        print(path)
        with open(path + '/encrypt.js') as f:
            for line in f:
                js_str = js_str + line
        
        default_exec = execjs.get()
        #print(js_str)
        ctx = default_exec.compile(js_str)
        pwd = ctx.call('encrypt',password, verifycode)
        return pwd

    def encryptTradePassword(self, tradepassword, uniqkey):
        print(threading.current_thread().name)
        js_str = ''
        path = os.path.dirname(os.path.abspath(__file__))
        with open(path + '/encrypt.js') as f:
            for line in f:
                js_str = js_str + line
        
        default_exec = execjs.get()
        ctx = default_exec.compile(js_str)
        pwd = ctx.call('encrypt2',tradepassword, uniqkey)
        return pwd

if __name__ == '__main__':
    encryptor = Encryptor(); 
    print(encryptor.encryptPassword("richard", '123456'))
    encryptor = Encryptor(); 
    print(encryptor.encrypt('123456', '2017-07-26 12:12:12'))