from flask import Flask,render_template,session,redirect,request
import random
app=Flask(__name__)
app.secret_key = '_5#2L"F4Q8z\n\xec]/'

@app.route("/")
def home():
    if 'random' not in session:
        randomNumber=random.randrange(0, 101)
        session["random"]=randomNumber
        session["answerNum"]=4
    print(session["random"])

    return render_template("index.html")

@app.route("/processing", methods=["POST"])
def process():
    
    if 'playagain' in request.form:
        session.clear()

    elif 'submit' in request.form:
        number=request.form["answer"]
        if int(number) >session["random"]:
            print("too high")
            session["answerNum"]=1
        elif int(number) <session["random"]:
            print("too low")
            session["answerNum"]=0
        else:
            print("exact")
            session["answerNum"]=2
            
        
    return redirect("/")



if __name__=="__main__":
    app.run(debug=True)