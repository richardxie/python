#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from flask import Flask, request, Response, url_for, json, jsonify
from yatang import Cookies, Signin, Session
from yatang.modules import SigninInfo
from tzj import Signin as TZJSignin
import utils, logging, base64
from utils.json_encoder import new_alchemy_encoder

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
    logger.debug(website +" signin info ")
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
