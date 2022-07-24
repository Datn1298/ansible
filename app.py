from flask import Flask
from audit import *
app = Flask(__name__)

@app.route('/audit')
def audit():
   object = audit_os("")
   return object

   # object = audit_permission_file("/etc/passwd", "", "-rw-r--r--")
   # return object
if __name__ == '__main__':
   app.run()