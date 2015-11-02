from flask import *
from jinja2 import TemplateNotFound
import hashlib
import uuid
import time, datetime
import os
from os import path
from werkzeug import secure_filename # for uploading files
from datetime import datetime
from collections import namedtuple
from extensions import mysql, mail
from flask_mail import Message
data = Blueprint('data', __name__, template_folder='templates')


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

def send_mail():
    msg = Message("Warning",
                  sender="cloudmanufacturing2015@gmail.com",
                  recipients=["chenxijessicacx@gmail.com"])
    mail.send(msg)

@data.route('/data', methods=['POST', 'GET'])
def getAlbums():
    if "username" in session:
        username = session["username"]
        if session_has_expired():
            remove_session()
            print "\n\nSESSION HAS EXPIRED!!!!\n\n"
            options = {
                "url": "/cloud/data",
                "message": "SESSION HAS EXPIRED!!!"
            }
            return render_template('auth_fail.html', **options)
        update_session_time()
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM Album WHERE username = %s''', (username,))
        albums=cur.fetchall()
        options = {
            "albums": albums,
            "username": username
        }
        return render_template('show_albums.html', **options)
    else:
        print "\n\n no session getAlbums"
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM Comment''')
        real_data=cur.fetchall()
        cur.execute('''SELECT * FROM User''')
        simulate_data=cur.fetchall()

        if not real_data or not simulate_data:
            return render_template('error.html', result="404 error No data")
        print real_data
        options = {
            "data": real_data,
            "simulate_data": simulate_data,
            "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        send_mail()
        return render_template('show_data.html', **options)
        




