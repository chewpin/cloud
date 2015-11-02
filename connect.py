
from flask import *
import pymssql

server = "cloudsubscriber.cfkf6u8wfyd.us-west-2.rds.amazonaws.com"
user = "fanzy"
password = "Cloud2015"
port = "1433"

conn = pymssql.connect(server, user, password, "CLOUDSUBSCRIBER", port)
cursor = conn.cursor()
cursor.execute("""
	SELECT @VERSION AS 'SQL Server Version'
)
""")
conn.close()
