from flask import *
from flask_mysqldb import MySQL
import smtplib
from email.message import EmailMessage

ob=Flask(__name__)

ob.secret_key="fsdfegdsfgd$@&g2342342"

ob.config['MYSQL_USER']='root'
ob.config['MYSQL_PASSWORD']=''
ob.config['MYSQL_DB']='electroniXhub'

mysql=MySQL(ob)

@ob.route("/")
def index():
    return render_template('admin/admin_index.html')

if __name__=='__main__':
    ob.run(debug=True,port=1424)
