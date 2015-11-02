from flask import *
from jinja2 import TemplateNotFound
import hashlib
import uuid
import time, datetime
from datetime import datetime


import os
from os import path
from werkzeug import secure_filename # for uploading files
from extensions import mysql

main = Blueprint('main', __name__, template_folder='templates')

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

@main.route("/return_")
def return_():
    function_name = request.args.get('function_name')
    return redirect( url_for('hello'))

@main.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        print "\nGET\nGET\nGET\n"
    if request.method == 'POST':
        print "add albums POST result op: " 
        print request.form.get('op')
        print "add albums POST result username: " 
        print request.form.get('username')
        print "add albums POST result title: " 
        print request.form.get('title')
    
    print "\n"
    if "username" in session:
        if session_has_expired():
            remove_session()
            print "\n\nSESSION HAS EXPIRED!!!!\n\n"
            options = {
                "message": "You're not logged in",
            }
        else:
            update_session_time()
            print "\n\nSESSION NOT EXPIRED\n\n"
            username = session['username']
            cur = mysql.connection.cursor()
            cur.execute('''SELECT Album.* FROM Album LEFT JOIN AlbumAccess ON Album.albumid=AlbumAccess.albumid WHERE Album.access=%s OR Album.username=%s OR AlbumAccess.username=%s ORDER BY username ASC''', ("public",username, username))
            albums=cur.fetchall()
            print albums
            options = {
                "message": ';)',
                "albums": albums
            }
    else:
        options = {
            "message": "Welcome",
        }
    return render_template('hello.html', **options)
