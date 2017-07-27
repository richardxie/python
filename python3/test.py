from utils import Encryptor, initSys
from conf import initConfig
from yatang import Cookies, Login, Loan
from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler

initSys()
initConfig()
encryptor = Encryptor(); 
print(encryptor.encryptPassword('richard', '123456'))
print(encryptor.encryptTradePassword('richard', '123456'))

cookie = Cookies("./")
cj = cookie.readCookie('richardxieq')

#login = Login()
#login.loginRequest('richardxieq','root1234')

opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
install_opener(opener)
print(Loan.loanRequest(opener, {"id":"1087550"}));

