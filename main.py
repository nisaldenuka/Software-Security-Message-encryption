from flask import Flask,render_template,request,redirect,url_for
import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb
import re
import hashlib
import GenerateSS
import EncryptDataSS
import DecryptSS

#print(hashlib.algorithms_guaranteed)
#h=hashlib.new("sha1")




# Replace these values with your XAMPP MySQL database credentials
#host = "localhost"
#user = "root"
#password = ""
#database = "SoftwareSecurity"

# Create a connection to the MySQL database
#conn = mysql.connector.connect(
   # host=host,
    #user=user,
    #password=password,
    #database=database
#)

# Create a cursor object to interact with the database
#cursor = conn.cursor()
app=Flask(__name__)


app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']=""
app.config['MYSQL_DB']="softwaresecurity"

mysql=MySQL(app)

@app.route('/')
def main():
    return render_template('Registration.html')


@app.route('/Registration',methods=['GET','POST'])
def Registration():
    if request.method == 'POST' and 'txtuname' in request.form and 'txtpw' in request.form and 'txtcpw' in request.form and 'role' in request.form:
        h=hashlib.new("sha1")
        email=request.form['txtuname']
        pw=request.form['txtpw']
        cpw=request.form['txtcpw']
        role=request.form['role']
        h.update(pw.encode())

        hashpw=h.hexdigest()
        cursor1=mysql.connection.cursor()

        cursor1.execute("SELECT email FROM user where email= %s",(email,))
        account=cursor1.fetchone()
        if pw==cpw:
            if account:
                mesage ='Account already exists !'

            elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
                mesage='Invalid Email'

            else:
                cursor1.execute("INSERT INTO user(email,password,type) VALUES (%s,%s,%s)",(email,hashpw,role))
                mysql.connection.commit()
                cursor1.close()
                mesage='Sucessfuly Registor'
                return render_template('Message.html')
        else:
           mesage='Password and confirm password not equal'  
        return render_template('Registration.html',mesage=mesage)      
    else:
         return render_template('Registration.html',mesage='')
@app.route('/Message',methods=['GET','POST'])
def Message():
    if request.method == 'POST' and 'msg' in request.form and  'role' in request.form:
        msg=request.form['msg']
        role=request.form['role']

        #cursor2=mysql.connection.cursor()
        GenerateSS.KeyGeneration()

        EncryptDataSS.Encryption(msg,role)
        return render_template('Message.html',mesage='Message sucessfuly Encrypted')
    else:
        return render_template('Message.html',mesage='')

@app.route('/Read',methods=['GET','POST'])
def Read():
    if request.method == 'POST' and 'txtuname' in request.form and 'txtpw' in request.form:
        h=hashlib.new("sha1")
        email=request.form['txtuname']
        pw=request.form['txtpw']
        h.update(pw.encode())

        hashpw=h.hexdigest()
        #return render_template('Read.html',Data=hashpw,mesage=email)
        cursor2=mysql.connection.cursor()
        cursor2.execute("SELECT email,password,type FROM user where email= %s and password= %s ",(email,hashpw))
        account=cursor2.fetchone()
        if account:
            #return render_template('Read.html',Data='winx',mesage='mesage')
            user_type = account[2]
            data= DecryptSS.Decryption(user_type)
            
            mesage ='Account already exists !'
            return render_template('Read.html',Data=data,mesage=" ")  
        else:
            return render_template('Read.html',Data='',mesage='Invalid Login ')    
    else:
        return render_template('Read.html',Data='',mesage='')
        
        

if __name__=="__main__":
    app.run()
