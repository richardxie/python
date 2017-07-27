import execjs, threading, os
class Encryptor: 
    def __init__(self, js_str = None):
        self.js_str = js_str
        pass

    def encrypt(self, password, timestamp):
        if self.js_str is None:
            self.js_str = ''
            path = os.path.dirname(os.path.abspath(__file__))
            print(path)
            with open(path + '/aes.js') as f:
                for line in f:
                    self.js_str = self.js_str + line

        default_exec = execjs.get()
        print(self.js_str)
        ctx = default_exec.compile(self.js_str)
        pwd = ctx.call('ytUtil.encrypt',password, timestamp)
        return pwd

    def encryptPassword(self, password, verifycode):
        if self.js_str is None:
            self.js_str = ''
            path = os.path.dirname(os.path.abspath(__file__))
            print(path)
            with open(path + '/encrypt.js') as f:
                for line in f:
                    self.js_str = self.js_str + line
        
        default_exec = execjs.get()
        print(self.js_str)
        ctx = default_exec.compile(self.js_str)
        pwd = ctx.call('encrypt',password, verifycode)
        return pwd

    def encryptTradePassword(self, tradepassword, uniqkey):
        print(threading.current_thread().name)
        if self.js_str is None:
            self.js_str = ''
            with open('encrypt.js') as f:
                for line in f:
                    self.js_str = self.js_str + line
        
        default_exec = execjs.get()
        ctx = default_exec.compile(self.js_str)
        pwd = ctx.call('encrypt2',tradepassword, uniqkey)
        return pwd

if __name__ == '__main__':
    encryptor = Encryptor(); 
    print(encryptor.encryptPassword("richard", '123456'))
    encryptor = Encryptor(); 
    print(encryptor.encrpyt('123456', '2017-07-26 12:12:12'))