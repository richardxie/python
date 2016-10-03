#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from flask import Flask, request, Response, url_for, json, jsonify
from urllib2 import HTTPCookieProcessor,build_opener,install_opener
from yatang import Cookies, Signin, Session
from yatang.modules import SigninInfo, UserInfo
from tzj import Signin as TZJSignin
import utils, logging, base64
from utils.json_encoder import new_alchemy_encoder
from hashlib import md5
from datetime import datetime

app = Flask(__name__)
logger = logging.getLogger("web")

@app.route("/")
def index():
    logger.info("index page!")
    data = {
        'page':'index'
            }
    resp = Response(json.dumps(data), status=200, mimetype="application/json")
    resp.headers['Link'] = 'http://abc.com'
    return resp

@app.route("/health")
def health():
    logger.info("health page!")
    data = {
        'page':'health',
        'state':'OK'
            }
    resp = Response(json.dumps(data), status=200, mimetype="application/json")
    resp.headers['Link'] = 'http://abc.com'
    return resp

"""
curl  -X POST -H "Content-Type:application/x-www-form-urlencoded" \
    -d 'username=richardxieq' -d 'password=tzjroot@2016' \
    http://localhost:8000/pyproj/tzj/signin
"""
@app.route("/<website>/signin", methods=['POST'])
def signin(website):
    if website == 'tzj':
        logger.debug("tzj signin request")
        name = request.form['username'] if request.form.has_key('username') else request.form['name']
        passwd = request.form['password']
        data = TZJSignin(base64.b64encode(name), base64.b64encode(passwd)).signin()
        resp = jsonify(data)
        resp.status_code = 200
        return resp
    else:
        logger.debug("yatang signin request")
        name = request.form['username'] if request.form.has_key('username') else request.form['name']
        passwd = request.form['password']
        cookies = Cookies("./")
        cookie = cookies.readCookie(name)
        if len(cookie) == 0:
            signin = Signin(name = name, password=passwd)
        else:
            signin = Signin(cookie = cookie, name = name)
        data = signin.signin()
        resp = jsonify(data)
        resp.status_code = 200
        return resp

@app.route("/<website>/signin", methods=['GET'])
def signininfo(website):
    logger.info(website +" signin info ")
    session = Session()
    query = session.query(SigninInfo).filter(SigninInfo.website == website)
    if query.count() == 0:
        return "No siginin information"
    else:
        info = json.dumps(query.all(), cls=new_alchemy_encoder(), check_circular=False, sort_keys=True)
        resp = Response(info, status=200, mimetype="application/json")
        return resp

@app.route("/<website>/signin/<username>", methods=['GET'])
def signininfodetail(website, username):
    logger.debug(website +" signin info for " + username)
    session = Session()
    query = session.query(SigninInfo).filter(SigninInfo.name == username, SigninInfo.website == website)
    if query.count() == 0:
        return "No siginin information"
    else:
        info = json.dumps(query.one(), cls=new_alchemy_encoder(), check_circular=False, sort_keys=True)
        resp = Response(info, status=200, mimetype="application/json")
        return resp

@app.route("/<website>/cookie", methods=['POST'])
def cookie(website):
    name = request.form['username'] if request.form.has_key('username') else request.form['name']
    passwd = request.form['password']
    cookies = Cookies("./")
    cookie = cookies.genCookie(name, passwd)
    resp = jsonify(cookies.dumpCookies(cookie))
    resp.status_code = 200
    return resp

@app.route("/<website>/cookie/<username>", methods=['Get'])
def query_cookie(website, username):
    cookies = Cookies("./")
    cookie = cookies.readCookie(username)
    cookies.dumpCookies(cookie)
    resp = jsonify(cookies.dumpCookies(cookie))
    resp.status_code = 200
    return resp

@app.route("/<website>/register", methods=['POST'])
def register(website):
    name = request.form['username'] if request.form.has_key('username') else request.form['name']
    passwd = request.form['password']
    session = Session()
    query = session.query(UserInfo).filter(UserInfo.name == name, UserInfo.website == website)
    if query.count() > 0:
        data = {
            'errorCode':'001',
            'errorMsg':'用户名已存在'
        }
        resp = jsonify(data)
        resp.status_code = 200
    else:
        import uuid
        user_info = UserInfo(
                id=str(uuid.uuid1()),
                website=website,                         
                name=name,
                password=md5(name + passwd + utils.Salt).hexdigest() if website == 'yt' else base64.b64encode(passwd)
            )
        session.add(user_info)
        session.commit()
        info = json.dumps(user_info, cls=new_alchemy_encoder(), check_circular=False, sort_keys=True)
        resp = Response(info, status=200, mimetype="application/json")
    return resp
   

@app.route("/<website>/resetpwd/<username>", methods=['POST'])
def reset_password(website, username):
    password = request.form['password']
    orginal_password = request.form['orginal_password']
    session = Session()
    query = session.query(UserInfo).filter(UserInfo.name == username, UserInfo.website == website)
    if query.count() == 0:
        data = {
            'errorCode':'002',
            'errorMsg':'用户名不存在'
        }
        info = json.dumps(data)
    else:
        user_info = query.one()
        md5_value = md5(username + orginal_password + utils.Salt).hexdigest()
        print md5_value
        print user_info.password
        if md5_value != user_info.password:
            data = {
                'errorCode':'003',
                'errorMsg':'原始密码不正确'
            }
            info = json.dumps(data)
        else:
            user_info.password = md5(username + password + utils.Salt).hexdigest()
            user_info.update_date = datetime.now()
            info = json.dumps(user_info, cls=new_alchemy_encoder(), check_circular=False, sort_keys=True)
            session.commit()
    resp = Response(info, status=200, mimetype="application/json")
    return resp

@app.route("/<website>/settradepwd/<username>", methods=['POST'])
def set_tradepassword(website, username):
    tradePassword = request.form['tradePassword']
    password = request.form['password']
    session = Session()
    query = session.query(UserInfo).filter(UserInfo.name == username, UserInfo.website == website)
    if query.count() == 0:
        data = {
            'errorCode':'002',
            'errorMsg':'用户名不存在'
        }
        info = json.dumps(data)
    else:
        #check password
        user_info = query.one()
        isPwdValid = True
        if website == 'yt':
            pwd = md5(username + password + utils.Salt).hexdigest()
            if pwd != user_info.password:
                isPwdValid = False
        else:
            if base64.b64encode(password) != user_info.password:
                isPwdValid = False

        if not isPwdValid:
            data = {
                        'errorCode':'003',
                        'errorMsg':'密码错误'
                    }
            info = json.dumps(data)
        else:
            user_info.trade_password = base64.b64encode(tradePassword)
            user_info.update_date = datetime.now()
            info = json.dumps(user_info, cls=new_alchemy_encoder(), check_circular=False, sort_keys=True)
            session.commit()
    resp = Response(info, status=200, mimetype="application/json")
    return resp

@app.route("/<website>/userid/<username>", methods=['GET'])
def user_id(website, username):
    cookies = Cookies("./")
    cookie = cookies.readCookie(username)
    opener = build_opener(HTTPCookieProcessor(cookie))
    install_opener(opener)
    session = Session()
    query = session.query(UserInfo).filter(UserInfo.name == username, UserInfo.website == website)
    if query.count() == 0:
        data = {
            'errorCode':'002',
            'errorMsg':'用户名不存在'
        }
        info = json.dumps(data)
    else:
        user_info = query.one()
        info = json.dumps(user_info, cls=new_alchemy_encoder(), check_circular=False, sort_keys=True)
    resp = Response(info, status=200, mimetype="application/json")
    return resp

with app.test_request_context():
    print(url_for('index'))
    print(url_for('health'))
    print(url_for('health', next='/'))
    print(url_for('signin', website='yt'))
    print(url_for('signininfo', website='yt', username='richardxieq'))
    pass

if __name__ == '__main__':
    utils.initSys()
    app.run(
            host="0.0.0.0",
            port=5000
            )
