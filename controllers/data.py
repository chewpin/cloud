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


def send_mail():
    msg = Message("Warning",
                  sender="cloudmanufacturing2015@gmail.com",
                  recipients=["chenxijessicacx@gmail.com"])
    mail.send(msg)

@data.route('/data', methods=['POST', 'GET'])
def getAlbums():
    if "username" in session:
        username = session["username"]
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
    else:
        print "\n\n no session getAlbums"
        options = {
            "message": "No access to data. Please log in"
        }
        return redirect( url_for('user.login'))
        




