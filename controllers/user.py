# from flask import Flask, render_template, url_for, request, session, g, redirect, send_from_directory, send_from_directory, Blueprint, abort

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

def hash_password(password):
    theHash = hashlib.sha1(password)
   # theHash.update(str(password))
    ans = theHash.hexdigest()
    ans = ans[0:20]
    print "the hashed password for : " + password + " is " + str(ans)
    return str(ans)

def update_session_time():
    session['lastactivity'] = datetime.now()

def remove_session():
    session.pop('username', None)
    session.pop('lastactivity', None)

def session_has_expired():
    end = datetime.now()
    start = session["lastactivity"]
    duration = end - start
    print "end had been inactive for " , end - start
    seconds = duration.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    if minutes >= 5:
        return True
    else:
        return False

def delete_file_from_picid(picid):
    format = get_pic_format_from_picid(picid)
    print "format: " + format
    print "about to delete picture with url: static/pictures/" + str(picid) + '.' + format
    path = str(picid) + '.' + format
    os.remove(os.path.join(UPLOAD_FOLDER, path))

def get_pic_format_from_picid(picid):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT format FROM Photo WHERE picid = %s''', (picid,))
    result=cur.fetchone()
    format = result[0]
    return format

def insert_user(username, firstname, lastname, email, password):
    conn = mysql.connection
    cur = conn.cursor()
    password = hash_password(password)
    print "insert_user hashed password is: " + password
    cur.execute('''INSERT INTO User (username, firstname, lastname, email, password) VALUES (%s, %s, %s, %s, %s)''', (username, firstname, lastname, email, password))
    result =cur.fetchall()
    print result
    conn.commit()

def is_user_unique(username):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute('''SELECT username FROM User WHERE username=%s''', (username,))
    result =cur.fetchall()
    if result:
        return False
    else:
        return True

def is_username_valid(username):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute('''SELECT username FROM User WHERE username=%s ''', (username,))
    result =cur.fetchall()
    if result:
        return True
    else:
        return False

def is_username_password_valid(username, password):
    conn = mysql.connection
    cur = conn.cursor()
    cur.execute('''SELECT username, password FROM User WHERE username=%s AND password = %s''', (username,password))
    result =cur.fetchall()
    if result:
        return True
    else:
        return False

@user.route('/user', methods=['POST', 'GET'])
def register():
    if "username" in session:
        update_session_time()
        print "/user but session already exists"
        return redirect(url_for('user.edit_user'))
    if request.method == 'GET':
        print "GET user.register"
    if request.method == 'POST':
        print "POST user.register"
        if request.method == 'POST' and "op" in request.form and request.form.get("op") == "register":
            username = request.form.get("username")
            firstname = request.form.get("firstname")
            lastname = request.form.get("lastname")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            print "username: ", username
            print "firstname: ", firstname
            print "lastname: ", lastname
            print "email: ", email
            print "password: ", password
            print "confirm: ", confirm
            if password != confirm:
                options = {
                    "action": "register",
                    "message": "password doesn't match! Please reenter information",
                    "register_title": "password doesn't match! Please reenter information"
                }
                return render_template('register.html', **options)
            print "WILL LOG IN 1"
            if not is_user_unique(username):
                options = {
                    "action": "register",
                    "message": "Username taken! Please select something else",
                    "register_title": "Username taken! Please select something else"
                }
                return render_template('register.html', **options)
            insert_user(username, firstname, lastname, email, password)
            cur = mysql.connection.cursor()
            cur.execute('''SELECT * FROM Album WHERE access=%s ORDER BY title ASC''', ("public",))
            albums=cur.fetchall()
            print albums
            options = {
                "message": "Please log in",
                "albums": albums
            }
            return render_template('hello.html', **options)
    print "user.register GET register"
    options = {
        "action": "register",
        "register_title": "Register"
    }
    return render_template('register.html', **options)

@user.route('/user/login', methods=['POST', 'GET'])
def login():
    if "username" in session:
        print "Already have logged in"
        update_session_time()
        options = {
            "url": "/cloud",
            "message": "Already have logged in"
        }
        return render_template('auth_fail.html', **options)
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
        password = hash_password(password)
        print " after hashing " + password
        if not is_username_valid(username):
            options = {
                "action": "login",
                "message": "username not valid",
                "url": url,
                "register_title": "username not valid"
            }
            return render_template('register.html', **options)
        if not is_username_password_valid(username, password):
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
            session['lastactivity'] = datetime.now()
        update_session_time()
        username = session['username']
        print "Session: ", username
        print session['lastactivity']

        return redirect(url)

        # cur = mysql.connection.cursor()
        # cur.execute('''SELECT Album.* FROM Album LEFT JOIN AlbumAccess ON Album.albumid=AlbumAccess.albumid WHERE Album.access=%s OR Album.username=%s OR AlbumAccess.username=%s ORDER BY username ASC''', ("public",username, username))
        # albums=cur.fetchall()
        # print albums
        # options = {
        #     "message": "Log in Successful",
        #     "albums": albums
        # }
        # return render_template('hello.html', **options)
    options = {
        "action": "login",
        "url": url,
        "register_title": "Log in"
    }
    return render_template('register.html', **options)

@user.route('/delete', methods=['POST'])
# @logged_in
def delete_user():
    if "username" not in session:
        print "username not in session can not delete user"
        options = {
            "url": "/cloud",
            "message": "username not in session can not delete user"
        }
        return render_template('auth_fail.html', **options)
    if request.method == 'POST' and 'op' in request.form and request.form.get('op') == 'delete':
        username = session["username"]
        conn = mysql.connection
        cur = conn.cursor()
        cur.execute('''DELETE FROM AlbumAccess WHERE username=%s''',(username,))
        conn.commit()   
        cur.execute('''SELECT albumid FROM Album WHERE username = %s''', (username,))
        albums=cur.fetchall()
        print "\nDELETEING ALBUM belonging to USER:"
        print username
        for album in albums:
            albumid = int(album[0])
            cur.execute('''DELETE FROM AlbumAccess WHERE albumid=%s''',(albumid,))
            cur.execute('''SELECT picid FROM Contain WHERE albumid=%s''',(albumid,))
            result=cur.fetchall()
            cur.execute('''DELETE FROM Contain WHERE albumid=%s''',(albumid,))
            picidarr = []
            for res in result:
                picidarr.append(res[0])
                print "picid to delete: " + str(res[0])
                delete_file_from_picid(res[0])
                cur.execute('''DELETE FROM Photo WHERE picid=%s''',(res[0],))
            cur.execute('''DELETE FROM Album WHERE albumid=%s''',(albumid,))
            conn.commit()
        cur.execute('''DELETE FROM User WHERE username=%s''',(username,))
        conn.commit()

        print " deleted user ", username
        session.pop('username', None)
        session.pop('lastactivity', None)
        cur.execute('''SELECT * FROM Album WHERE access=%s OR username=%s ORDER BY username ASC''', ("public",username))
        albums=cur.fetchall()
        print albums
        options = {
            "message": "You're not logged in",
        }
        return render_template('hello.html', **options)
    return render_template('hello.html')

@user.route('/user/edit', methods=['POST', 'GET'])
# @logged_in
def edit_user():
    print "IN edit_user"
    url = "/225x7i1wcdi/user/edit"
    if "username" not in session:
        print "username not in session"
        options = {
            "url": "/cloud/user/edit",
            "message": "Must authenticate to view this page"
        }
        return render_template('auth_fail.html', **options)
    if "username" in session:
        if session_has_expired():
            remove_session()
            print "\n\nSESSION HAS EXPIRED!!!!\n\n"
            options = {
                "url": "/cloud/user/edit",
                "message": "SESSION HAS EXPIRED!!!"
            }
            return render_template('auth_fail.html', **options)
        else:
            update_session_time()
            print "\n\nSESSION NOT EXPIRED\n\n"

    print "Edit!"
    # if form.validate_on_submit():
    if request.method == 'POST' and 'op' in request.form and request.form.get('op') == 'edit':
        print "Edit success"
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        email = request.form.get("email")
        if "username" in session:
            print "username in session: ", session["username"]
            username = session["username"]
            print "in edit user password " + password
            password = hash_password(password)
            print "after hashing " + password
            conn = mysql.connection
            cur = conn.cursor()
            cur.execute('''UPDATE User SET firstname=%s, lastname=%s, email=%s, password=%s WHERE username=%s''', (firstname, lastname, email, password, username))
            result =cur.fetchall()
            print result
            conn.commit()
            cur = mysql.connection.cursor()
            cur.execute('''SELECT Album.* FROM Album LEFT JOIN AlbumAccess ON Album.albumid=AlbumAccess.albumid WHERE Album.access=%s OR Album.username=%s OR AlbumAccess.username=%s ORDER BY username ASC''', ("public",username, username))
            albums=cur.fetchall()
            print albums
            options = {
                "message": "edit user %s" % username,
                "albums": albums
            }
        return render_template('hello.html', **options)
    print "username in session: "
    username = session["username"]
    update_session_time()
    options = {
        "action": "edit_user",
        "username": username,
        "register_title": "Register"
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
        session.pop('lastactivity', None)
    options = {
        "message": "You're not logged in",
    }
    return render_template('hello.html', **options)
