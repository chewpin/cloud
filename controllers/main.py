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



@main.route("/return_")
def return_():
    function_name = request.args.get('function_name')
    return redirect( url_for('hello'))

@main.route("/", methods=['GET', 'POST'])
def hello():
    if "username" in session:
        options = {
            "message": ' '
        }
    else:
        options = {
            "message": "Welcome",
        }
    return render_template('hello.html', **options)
