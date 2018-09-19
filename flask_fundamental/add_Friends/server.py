from flask import Flask,render_template,redirect,request

from mysqlconnection import connectToMySQL
app = Flask(__name__)

mysql = connectToMySQL('friends_db')

@app.route("/")
def home():

    friendsData=mysql.query_db("SELECT first_name,last_name,occupation FROM friends;")
    return render_template("index.html", friendData=friendsData)
    

@app.route("/createFriend",methods=["POST"])
def createFriend():

    # create query to add friends
    query="INSERT INTO friends(first_name,last_name,occupation) VALUES (%(firstname)s,%(lastname)s,%(occupation)s);"
    data={
    'firstname':request.form["firstname"],
    'lastname':request.form["lastname"],
    'occupation':request.form["occupation"]
    }
    mysql.query_db(query,data)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)