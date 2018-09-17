from flask import Flask,render_template,request,redirect,session,flash
import re

app=Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
UpperCasePassword_REGEX=re.compile(r'^(?=.*?[A-Z])')
NumericValue_REGEX=re.compile(r'^(?=.*?[0-9])')
date_REGEX=re.compile(r'^(0?[1-9]|[12][0-9]|3[01])[\/\-](0?[1-9]|1[012])[\/\-](199[0-9]|200[0-9]|201[0-9])$')


@app.route("/")
def loginPage():
    
    return render_template("index.html")


@app.route("/user",methods=['POST'])
def createUser():
    
    # first name validation
    if len(request.form["firstname"])<1:
        flash("please provide a name",'error')
    elif len(request.form["firstname"])<3:
        flash("first name is too short. Should be atleast 3 characters",'error')
    else:
        session["firstname"]=request.form["firstname"]

       # last name validation
    if len(request.form["lastname"])<1:
        flash("please provide a last name",'error')
    elif len(request.form["lastname"])<3:
        flash("last name is too short. Should be atleast 3 characters","error")
    else:
        session["lastname"]=request.form["lastname"]

    # email validation
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!",'error')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", 'error')
    


    #password validation

    if len(request.form["password"])<1:
        flash("please provide a password", 'error')
    elif len(request.form["password"])<8:
        flash("password is too short. Should be atleast 8 characters", 'error')
    elif not UpperCasePassword_REGEX.match(request.form['password']) :
        flash("at least one uppercase letter", 'error')
    elif not NumericValue_REGEX.match(request.form['password']) :
        flash("at least one number", 'error')

    #confirm passwrod validation

    if request.form["confirmpassword"]!=request.form["password"]:
        flash("Password does not match", 'error')

    # confirm data validation
    if not date_REGEX.match(request.form['birthday']) :
        flash("invalid date", 'error')



    if '_flashes' in session.keys():
        return redirect("/")
        
    else:
        session["userInfo"]=request.form
        return redirect("/result")
        

@app.route("/result")
def successLogin():
    return render_template("success.html")



@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")



if __name__=="__main__":
    app.run(debug=True)