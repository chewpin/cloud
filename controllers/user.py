import config
login_username = config.LOGIN_USERNAME
login_password = config.LOGIN_PASSWORD
from extensions import mysql
from flask import *
# from flask_wtf import Form
from jinja2 import TemplateNotFound
import hashlib
import uuid
import time, datetime
import os
from os import path
from functools import wraps
from datetime import datetime

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextField, BooleanField, PasswordField
from wtforms.validators import *

user = Blueprint('user', __name__, template_folder='templates')


def remove_session():
    session.pop('username', None)
    session.pop('lastactivity', None)

@user.route('/user/login', methods=['POST', 'GET'])
def login():
    if "username" in session:
        print "Already have logged in"
        options = {
            "message": "Already have logged in"
        }
        return render_template('hello.html', **options)
    url = "/cloud"
    print "LOG IN!!!"
    if "url" in request.args:
        url = request.args.get("url")
        print url
    if request.method == 'POST':
        # if not form:
        if "op" not in request.form or request.form.get("op") != "login":
            print "op not in form or form.op.data != login"
            options = {
                "action": "login",
                "message": "op not in form or form.op.data != login",
                "url": url,
                "register_title": "op not in form or form.op.data != login"
            }
            return render_template('register.html', **options)

        username = request.form.get("username")
        password = request.form.get("password")
        print "password in register: " + password
        # password = hash_password(password)
        print " after hashing " + password
        if not username == login_username:
            options = {
                "action": "login",
                "message": "username not valid",
                "url": url,
                "register_title": "username not valid"
            }
            return render_template('register.html', **options)
        if not password == login_password:
            options = {
                "action": "login",
                "message": "username and password combo not valid",
                "url": url,
                "register_title": "username and password combo not valid"
            }
            return render_template('register.html', **options)
        if "username" not in session:
            print "\nNEW SESSION POST user.login"
            print "username: ", username
            print "password: ", password
            print "WILL create session!!! 3"
            session['username'] = username
        username = session['username']
        print "Session: ", username

        return redirect(url)

    options = {
        "action": "login",
        "url": url,
        "register_title": "Log in"
    }
    return render_template('register.html', **options)

@user.route('/logout')
# @logged_in
def logout():
    # remove the username from the session if it's there
    print "LOG OUT!"
    if "username" in session:
        print "username in session: "
        print session["username"]
        session.pop('username', None)
    options = {
        "message": "You're not logged in",
    }
    return render_template('hello.html', **options)
