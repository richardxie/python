#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-

from flask import Flask, request
from yatang import Cookies, Signin
import utils, logging

app = Flask(__name__)
logger = logging.getLogger("web")

@app.route("/")
def index():
    logger.info("index page!")
    return 'Index Page'

@app.route("/health")
def health():
    logger.info("health page!")
    return "OK"

@app.route("/yt/signin", methods=['POST'])
def ytsignin():
    logger.debug("yatang signin request")
    name = request.form['username']
    passwd = request.form['password']
    cookies = Cookies("./")
    cookie = cookies.readCookie(name)
    if len(cookie) == 0:
        signin = Signin(name = name, password=passwd)
    else:
        signin = Signin(cookie = cookie)
    return signin.signin()

if __name__ == '__main__':
    utils.initSys()
    app.run(
            host="0.0.0.0",
            port=5000
            )
    