from flask import Flask,render_template,request,redirect,session

app=Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def loginPage():
    
    return render_template("formPage.html")


@app.route("/user",methods=['POST'])
def createUser():
    print("got the form")
    print(request.form)

    session["firstname"]=request.form["firstname"]
    session["lastname"]=request.form["lastname"]
    session["location"]=request.form["Location"]
    session["language"]=request.form["language"]
    session["textarea"]=request.form["textarea"]
    return redirect("/result")
    

@app.route("/result")
def successLogin():
    return render_template("success.html")

@app.route("/danger")
def danger():
    print("a user name:"+session["firstname"]+" "+session["lastname"]+" tried to visit /danger")
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)