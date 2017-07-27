#!/usr/bin/python2.7
# ！-*- coding: utf-8 -*-
from flask_script import Manager

from webservice import app

manager = Manager(app)

@manager.command
def hello():
    print "hello"

if __name__ == "__main__":
    manager.run()