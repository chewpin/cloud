from flask import *
import config
import copy
import datetime
import threading
import pymssql
from extensions import mail
from flask_mail import Message

main = Blueprint('main', __name__, template_folder='templates')

def remove_session():
    session.pop('username', None)
    session.pop('lastactivity', None)

@main.route("/", methods=['GET'])
def getDashboard():
    if "username" not in session:
        return redirect(url_for('user.login'))

    conn = pymssql.connect(config.server, config.user, config.password, config.database)
    # conn = pymssql.connect(server=config.MSSQL_SERVER, user=config.MSSQL_USER, password=config.MSSQL_PASSWORD, database=config.MSSQL_DB)
    cursor = conn.cursor(as_dict=True)
    cursor.execute("SELECT TagName, TagValue FROM dbo.Tag")
    data = cursor.fetchall()
    print(data)
    now = datetime.datetime.now().strftime("%B %d %Y %I:%M:%S%p")
    simulate_data = copy.deepcopy(data)
    simulate_data[0]['TagValue'] = 100
    simulate_data[2]['TagValue'] = 1
    return render_template('dashboard.html', data=data, simulate_data=simulate_data, now=now)

@main.route("/send", methods=['GET'])
def sendMail():
    msg = Message("Warning",
                  sender="cloudmanufacturing2015@gmail.com",
                  recipients=["chenxijessicacx@gmail.com"])
    @copy_current_request_context
    def send_email(msg):
        mail.send(msg)
    sender = threading.Thread(name='mail_sender', target=send_email, args=(msg,))
    sender.start()
    return redirect(url_for('main.getDashboard'))