from flask import Flask,render_template,session,request,redirect,flash
from flask_bcrypt import Bcrypt    
import re    
from DatabaseConnection import connectToMySQL
import requests
import json
app = Flask(__name__)        
bcrypt = Bcrypt(app)  

mysql = connectToMySQL('User_db')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
UpperCasePassword_REGEX=re.compile(r'^(?=.*?[A-Z])')
NumericValue_REGEX=re.compile(r'^(?=.*?[0-9])')
date_REGEX=re.compile(r'^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-](199[0-9]|200[0-9]|201[0-9])$')
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'


Countries_url= requests.get('https://restcountries.eu/rest/v2/all?fields=name;')
Countries_data=Countries_url.json()



@app.route("/")
def registration():
    
    return render_template("registration.html",Countries_data=Countries_data)




@app.route("/process", methods=['POST'])
def process():
    user_data=request.form

    #firstname validation
    if len(user_data['firstname'])<1:
        flash("First name cannot be blank!!",'firstname')
    elif user_data['firstname'].isalpha()==False:
        flash("Only letters in the first name",'firstname')
    elif len(user_data['firstname'])>20:
        flash("First name is too long!!",'firstname')
    elif len(user_data['firstname'])<2:
        flash("First name should be atleat 2 characters",'firstname')
    else:
        session['firstname']=user_data["firstname"]

    #Lastname validation
    if len(user_data['lastname'])<1:
        flash("Last name cannot be blank!!",'lastname')
    elif user_data['lastname'].isalpha()==False:
        flash("Only letters in the Last name",'lastname')
    elif len(user_data['lastname'])<2:
        flash("Last name should be atleat 2 characters",'lastname')
    elif len(user_data['lastname'])>30:
        flash("Last name is too long!!",'lastname')
    else:
        session['lastname']=user_data["lastname"]

    # email validation
    if len(user_data['email']) < 1:
        flash("Email cannot be blank!",'email')
    elif not EMAIL_REGEX.match(user_data['email']):
        flash("Invalid Email Address!", 'email')
    else:
        session['email']=user_data["email"]


    #password validation

    if len(user_data["password"])<1:
        flash("please provide a password", 'password')
    elif len(user_data["password"])<8:
        flash("password is too short. Should be atleast 8 characters", 'password')
    elif not UpperCasePassword_REGEX.match(user_data['password']) :
        flash("at least one uppercase letter", 'password')
    elif not NumericValue_REGEX.match(user_data['password']) :
        flash("at least one number", 'password')

    #confirm passwrod validation

    if user_data["confirmpassword"]!=user_data["password"]:
        flash("Password does not match", 'confirmpassword')


    #Country Validation
    if user_data['country']=="":
        flash("Please provide a Country",'country')
    else:
        session['country']=user_data["country"]

    # Language Validation
    if user_data['language']=="":
        flash("Please Provide your Favorite Language")


    if '_flashes' in session.keys():
        return redirect("/")
        
    else:
        
        query="INSERT INTO users(firstname,lastname,email,favorite_language,password,country,created_at,updated_at) VALUES(%(firstname)s,%(lastname)s,%(email)s,%(language)s,%(password)s,%(country)s,NOW(),NOW());"
        
        password_hash=bcrypt.generate_password_hash(user_data['password'])
        
        data={
            'firstname':user_data['firstname'],
            'lastname':user_data['lastname'],
            'password':password_hash,
            'email':user_data['email'],
            'country':user_data['country'],
            'language':user_data['language']
        }

        mysql.query_db(query,data)
        session.clear()
        
        return redirect("/login")


@app.route("/login")
def login():
    
    return render_template("login.html")


@app.route("/loginProcess",methods=['POST'])
def loginProcess():
    # clear session
    if 'user_info' in session:
        session.clear()

    user_data={
        'email':request.form['email'],
        'password':request.form['password']
    }
    query="SELECT password,firstname,user_id FROM users WHERE email=%(email)s"

    # query database
    match_user=mysql.query_db(query,user_data)

    # checking if user exits and if allowed to log in
    if len(match_user)==0:
        flash("Invalid Email or Password")
        return redirect("/login")
    else:
        
        if bcrypt.check_password_hash(match_user[0]['password'], request.form['password']):
            IsLoggedIn=match_user[0]['firstname']
            session['user_info']=IsLoggedIn
            return redirect("/dashboard")
        else:
            flash("Invalid Email or Password")
            return redirect("/login")   

@app.route("/dashboard")
def dashboard():

    if 'user_info' not in session:
        return redirect("/login")
    else:
        if session['user_info']:
            return render_template("dashboard.html")
        else:
            return redirect("/login")

    
if __name__=="__main__":
    app.run(debug=True)