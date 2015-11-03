from extensions import mail, mysql
import controllers
from flask import *
from jinja2 import TemplateNotFound
import hashlib
import uuid
import time, datetime
from datetime import timedelta
import os
from os import path
from werkzeug import secure_filename # for uploading files
from flask_mail import Mail

import pymssql



app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(controllers.main, url_prefix='/cloud')
app.register_blueprint(controllers.data, url_prefix='/cloud')
app.register_blueprint(controllers.user, url_prefix='/cloud')

mysql.init_app(app)
mail.init_app(app)




# set the secret key.  keep this really secret:
app.secret_key = os.urandom(24)


if __name__ == "__main__":
    app.run(debug=True)
