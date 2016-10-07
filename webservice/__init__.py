#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-
from flask import Flask, request, Response, url_for, json, jsonify
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

import os, sys
sys.path.append(os.path.dirname(__file__))

def make_json_app(import_name, **kwargs):
    """
    Creates a JSON-oriented Flask app.

    All error responses that you don't specifically
    manage yourself will have application/json content
    type, and will contain JSON like this (just an example):

    { "message": "405: Method Not Allowed" }
    """
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app
app = make_json_app(__name__)

import webservice.web

with app.test_request_context():
    print(url_for('index'))
    print(url_for('health'))
    print(url_for('health', next='/'))
    print(url_for('signin', website='yt'))
    print(url_for('signininfo', website='yt', username='richardxieq'))
    print(url_for('createRules', website='yt'))
    pass