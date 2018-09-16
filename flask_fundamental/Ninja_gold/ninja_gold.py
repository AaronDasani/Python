from flask import Flask,render_template,session,redirect,request
import random
import datetime
import time

app=Flask(__name__)
app.secret_key = '_5#2L"F4Q8z\n\xec]/'

data_list=[]

@app.route("/")
def home():
    if 'coins' not in session:
        session["coins"]=0
       
    if 'data' not in session:
        session["data"]=[]

    return render_template("index.html")

@app.route("/process_money",methods=["POST"])
def process():

    session["property"]=request.form["building"]
    data_list.reverse()

    session["theTime"]=datetime.datetime.now().strftime("20%y/%m/%d %I:%M %p")

    if session["property"]=="farm":
        coins=random.randrange(10, 21)
        session["coins"]=session["coins"]+coins
        data_list.append({session["property"]:coins})
        

    elif session["property"]=="cave":
        coins=random.randrange(5, 11)
        session["coins"]=session["coins"]+coins
        data_list.append({session["property"]:coins})
        

    elif session["property"]=="house":
        coins=random.randrange(2, 6)
        session["coins"]=session["coins"]+coins
        data_list.append({session["property"]:coins})
        

    elif session["property"]=="casino":
        odds=random.randrange(0,2)
        coins=random.randrange(0, 51)   
        if odds==1:  
            session["coins"]=session["coins"]+coins
            data_list.append({session["property"]:coins})
            

        else:
            session["coins"]=session["coins"]-coins
            data_list.append({session["property"]:-coins})
            

    data_list.reverse()
    session["data"]=data_list
   


    return redirect("/")

@app.route("/delete")
def delete():
    session.clear()
    data_list.clear()
    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)