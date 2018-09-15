from flask import Flask,render_template,session,redirect,request
app=Flask(__name__)
app.secret_key = '_5#2L"F4Q8z\n\xec]/'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/procceedToCheckout",methods=["POST"])
def proceed():
    a_list={}
    product_sum=0
    session["array"]=request.form

    for key,value in session["array"].items():
        if int(value)>0:
            product_sum+=int(value)
            a_list.update({key:value})

    session["array"]=a_list
    session["sum"]=product_sum

    return redirect("/checkout")

@app.route("/checkout")
def checkout():
    
    return render_template("checkout.html")

@app.route("/checkoutcomplete" ,methods=["POST"])
def checkoutcomplete():
    # print(request.form)
    session["firstname"]=request.form["firstName"]
    session["lastname"]=request.form["lastName"]
    session["Studentid"]=request.form["Studentid"]
    session["email"]=request.form["email"]
    
    return redirect("/success")
    
@app.route("/success")
def success():
    
    return render_template("success.html")

if __name__=="__main__":
    app.run(debug=True)
