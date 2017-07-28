from utils import Encryptor, initSys
from conf import initConfig
from yatang import Cookies, Login, Loan
from urllib.request import HTTPCookieProcessor,Request,build_opener,install_opener,HTTPRedirectHandler

initSys()
initConfig()
encryptor = Encryptor(); 
print(encryptor.encryptPassword('yourname', 'yourpasswrod'))
print(encryptor.encryptTradePassword('yourname', 'yourpasswrod'))

cookie = Cookies("./")
cj = cookie.readCookie('yourname')

#login = Login()
#login.loginRequest('yourname','yourpasswrod')

opener = build_opener(HTTPCookieProcessor(cj), HTTPRedirectHandler())
install_opener(opener)
print(Loan.loanRequest(opener, {"id":"1087550"}));

