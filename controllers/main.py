from flask import *
import config
import pymssql

from datetime import datetime
from extensions import mysql

main = Blueprint('main', __name__, template_folder='templates')

def remove_session():
    session.pop('username', None)
    session.pop('lastactivity', None)

@main.route("/", methods=['GET'])
def getDashboard():
    if "username" not in session:
        return redirect(url_for('user.login'))
    conn = pymssql.connect(server=config.MSSQL_SERVER, user=config.MSSQL_USER, password=config.MYSQL_PASSWORD, database=config.MSSQL_DB)
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT TagName, TagValue FROM dbo.Tag")
    data = cursor.fetchall()
    return render_template('dashboard.html', data=data)

