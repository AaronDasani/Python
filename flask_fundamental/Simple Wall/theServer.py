from flask import Flask,render_template,session,request,redirect,flash
from flask_bcrypt import Bcrypt    
import re    
from DatabaseConnection import connectToMySQL
import datetime

app = Flask(__name__)        
bcrypt = Bcrypt(app)  

mysql = connectToMySQL('wall_user_db')

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
        
        query="INSERT INTO users(firstname,lastname,email,password,created_at,updated_at) VALUES(%(firstname)s,%(lastname)s,%(email)s,%(password)s,NOW(),NOW());"
        
        password_hash=bcrypt.generate_password_hash(user_data['password'])
        
        data={
            'firstname':user_data['firstname'],
            'lastname':user_data['lastname'],
            'password':password_hash,
            'email':user_data['email'],
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
            session['current_user']=match_user[0]['user_id']
            return redirect("/wall")
        else:
            flash("Invalid Email or Password")
            return redirect("/login")   

@app.route("/wall")
def dashboard():

    if 'user_info' not in session:
        return redirect("/login")
    else:
        if session['user_info']:

            # getting infomation from current user
            query="SELECT * FROM messages WHERE Users_user_id= %(current_user)s"
            data={
                'current_user':session['current_user']
            }

            current_user_posts=mysql.query_db(query,data)

            # getting the information of users from users table so we can message only people who is in the database
            all_user=mysql.query_db("SELECT user_id,firstname FROM users")

            return render_template("wall.html",current_user= session['current_user'],all_user=all_user,posts=current_user_posts)
        else:
            return redirect("/login")


@app.route("/createpost",methods=['POST'])
def newpost():
    
    # adding message to database
    query="INSERT INTO messages(content,Users_user_id,sender_name,created_at,updated_at) Value(%(message)s,%(recipient_id)s,%(sender_name)s,NOW(),NOW())"
    
    data={
        'message':request.form['textarea'],
        'recipient_id':request.form['user_id'],
        'sender_name': session['user_info']
    }

    mysql.query_db(query,data)

    # counting how many message was sent
    if 'number_of_message' not in session:
        session['number_of_message']=0
    session['number_of_message']=session['number_of_message']+1


    return redirect("/wall")


@app.route("/deletepost/<int:post_id>",methods=['POST'])
def delete(post_id):

    print(post_id)
    query="DELETE FROM messages WHERE (post_id = '%(deletePost)s');"
    data={
        'deletePost':post_id
    }
    mysql.query_db(query,data)

    return redirect("/wall")


@app.route("/logout")
def logout():
    
    session.clear()
    return redirect("/login")



if __name__=="__main__":
    app.run(debug=True)