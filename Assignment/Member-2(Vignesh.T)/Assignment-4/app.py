from flask import *
import os
import ibm_db


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;PROTOCOL=TCPIP;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=prm92612;PWD=aW3A18gUT3mCMGBh;", "", "")


app=Flask(__name__) 
app.secret_key = 'your secret key'

@app.route("/")
def signin():

    if request.method == 'POST':

        email= request.form['email']
        password = request.form['password']

        sql = "SELECT * FROM signin WHERE name =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)

        return render_template('home.html', msg="Login Successfuly..")
    
    else:
        return render_template('signin.html', msg="Login Failed..")

@app.route("/signup")
def signup():
    
  if request.method == 'POST':

    fname = request.form['fname']
    lname = request.form['lname']
    email= request.form['email']
    pwd = request.form['pwd']


    sql = "SELECT * FROM signin WHERE email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,3,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
      return render_template('signin.html', msg="You are already a member, please login using your details")
    else:
      insert_sql = "INSERT INTO signup VALUES (?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, fname)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, pwd)
      ibm_db.bind_param(prep_stmt, 4, lname)
      ibm_db.execute(prep_stmt)
    
  return render_template('signup.html', msg="Signin Successfuly..")

@app.route("/home")
def homepage():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/appointment")
def Appointment():
    try:
        if request.method == 'POST':

            name = request.form['name']
            email = request.form['email']
            phonenumber = request.form['phonenumber']
            message = request.form['message']            
            save(name,email,phonenumber,message)
      
        return render_template('appointment.html')
    except:
        return render_template('home.html',"Connection Failed")

def save(name,email,phonenumber,message):
    save_appointment = "INSERT INTO appointment_db VALUES({},{},{},{})".format(name,email,phonenumber,message)
    ibm_db.exec_immediate(conn, save_appointment)

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message= Mail(from_email='customerregistry@gmail.com',
               to_emails=['s_msg'],
               subject='Your Request is Registered',
               plain_text_content='We will consider your request',
               html_content='<strong>ThankYou</strong>' )

@app.route("/customer_service")
def customer_service():
    try:
        if request.method == 'POST':

            s_name = request.form['s_name']
            s_email = request.form['s_email']
            s_msg = request.form['s_msg']
            insert_sql = "INSERT INTO contact VALUES (?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, s_name)
            ibm_db.bind_param(prep_stmt, 2, s_email)
            ibm_db.bind_param(prep_stmt, 3, s_msg)
            ibm_db.execute(prep_stmt)

            sg= SendGridAPIClient(os.environ['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'])
            response=sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
            
        return render_template('customer_service.html')
    except:
        return "Connection Failed"
    


if __name__=="__main__":
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0',port=port) 