from flask import Flask,render_template,session,request,redirect,flash
from flask_bcrypt import Bcrypt    
import re    
from DatabaseConnection import connectToMySQL
import datetime

app = Flask(__name__)        
bcrypt = Bcrypt(app)  

mysql = connectToMySQL('Admin_db')

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
UpperCasePassword_REGEX=re.compile(r'^(?=.*?[A-Z])')
NumericValue_REGEX=re.compile(r'^(?=.*?[0-9])')
date_REGEX=re.compile(r'^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-](199[0-9]|200[0-9]|201[0-9])$')
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'




@app.route("/")
def registration():
    
    return render_template("registration.html")

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


    if '_flashes' in session.keys():
        return redirect("/")
        
    else:
        
        query="INSERT INTO users(firstname,lastname,email,user_level,password,created_at,updated_at) VALUES(%(firstname)s,%(lastname)s,%(email)s,%(user_level)s,%(password)s,NOW(),NOW());"
        
        password_hash=bcrypt.generate_password_hash(user_data['password'])
        
        data={
            'firstname':user_data['firstname'],
            'lastname':user_data['lastname'],
            'password':password_hash,
            'email':user_data['email'],
            'user_level':0
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
    query="SELECT password,firstname,user_id,user_level FROM users WHERE email=%(email)s"

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
            session['current_user']=match_user[0]['user_id']

            if match_user[0]['user_level']==1:
                return redirect("/Admin")
            else:
                return redirect("/normalUser")
        else:
            flash("Invalid Email or Password")
            return redirect("/login")   

@app.route("/Admin")
def dashboard():

    if 'user_info' not in session:
        return redirect("/login")
    else:
        if session['user_info']:

            all_user=mysql.query_db("SELECT * FROM users")

            return render_template("Admin.html",all_user=all_user)
        else:
            return redirect("/login")


@app.route("/normalUser")
def normalUser():

    return render_template("normalUser.html")



@app.route("/adminProcess/<int:user_id>",methods=['POST'])
def delete(user_id):

    print(user_id)

    # remove user
    if request.form['button']=='remove':
        query="DELETE FROM users WHERE (user_id = "+str(user_id)+");"
        mysql.query_db(query)

    #remove Admin Access
    elif request.form['button']=='removeAccess':

        query="UPDATE users SET user_level = 0 WHERE (user_id ="+str(user_id)+");"
        mysql.query_db(query)

    # Make Admin
    elif request.form['button']=='makeAdmin':

        query="UPDATE users SET user_level = 1 WHERE (user_id ="+str(user_id)+");"
        mysql.query_db(query)

    return redirect("/Admin")


@app.route("/logout")
def logout():
    
    session.clear()
    return redirect("/login")



if __name__=="__main__":
    app.run(debug=True)