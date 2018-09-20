from flask import Flask,render_template,session,request,redirect,flash
from flask_bcrypt import Bcrypt    
import re    
from databaseConnect import connectToMySQL

app = Flask(__name__)        
bcrypt = Bcrypt(app)  

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

mysql = connectToMySQL('email_db')

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/process", methods=['POST'])
def process():
    email=request.form['email']
    databaseEmails=mysql.query_db("SELECT email FROM emails;")
    print(databaseEmails)
    print(email)

    if len(email) < 1:
        flash("Email cannot be blank!")
    elif not EMAIL_REGEX.match(email):
        flash("Invalid Email Address!")
    
    for index in databaseEmails:
        if index['email']==email:
            flash("Email Address already taken!")
            break

    

    if '_flashes' in session.keys():
        return redirect("/")
    else:
        query="INSERT INTO emails(email,created_at,updated_at) VALUES (%(email)s, NOW(),NOW())"
        data={'email':email}
        mysql.query_db(query,data)
        
        return redirect("/success")
        

@app.route("/success")
def success():

    emails=mysql.query_db("SELECT email_id,email,created_at FROM emails;")
    # print(emails)
    return render_template("success.html", emails=emails)


@app.route("/delete/<int:post_id>", methods=['POST'])
def delete(post_id):
    query="DELETE FROM emails WHERE (email_id = '%(deleteEmail)s');"
    data={
        'deleteEmail':post_id
    }
    mysql.query_db(query,data)
    return redirect("/success")

if __name__=="__main__":
    app.run(debug=True)