from flask import Flask,render_template,session,redirect,request
app=Flask(__name__)
app.secret_key = '_5#2L"F4Q8z\n\xec]/'

@app.route("/")
def home():
    counts=1 
    if 'count' not in session:
        session['count'] = 0

    session["count"]=session["count"]+counts
    return render_template("index.html")

@app.route("/destroy_session")
def clear():
    session.clear()
    return redirect("/")

@app.route("/processing",methods=["POST"])
def processing():
    if 'button1' in request.form:
        return redirect("/add")
    elif 'button2' in request.form:
        return redirect("/reset")
    


@app.route("/add")
def add():
    session["count"]=session["count"]+1
    return redirect("/")

@app.route("/reset")
def delete():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)