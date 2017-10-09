from utils import Encryptor, initSys, Salt
from conf import initConfig
from yatang import Session
from yatang.modules import UserInfo
from uuid import uuid1
from hashlib import md5
from base64 import b64encode
from datetime import datetime
initSys()
#initConfig()
name = 'yourname'
passwd = 'yourpsw'
tradePassword = 'tradepws'
userid = 'id'
website = 'yt'
session = Session()
query = session.query(UserInfo).filter(UserInfo.name == name, UserInfo.website == website)
if query.count() == 0:
    user_info = UserInfo(
                id=str(uuid1()),
                user_id = userid,
                website='yt',                         
                name= name,
                password=md5((name + passwd + Salt).encode("UTF-8")).hexdigest(),
                trade_password=b64encode(tradePassword.encode('UTF-8'))
    )
    session.add(user_info)
    session.commit()
else:
    user_info = query.one()
    user_info.trade_password=b64encode(tradePassword.encode('UTF-8'))
    user_info.user_id = userid
    user_info.update_date = datetime.now()
    session.commit()

