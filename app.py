from flask import Flask
# from audit import *
from audit_ssh import *
from audit_datetime import *
from audit_password_policy import *
from audit_monitor import audit_monitor
from audit_log import audit_log
from audit_port import audit_port_open
from audit_network_connection import audit_network_connection

app = Flask(__name__)

@app.route('/audit')
def audit():
   object = audit_network_connection("")
   return object

if __name__ == '__main__':
   app.run()