from flask import Flask,render_template,request,redirect
from databaseConnection import connectToMySQL
import json

app = Flask(__name__)

mysql = connectToMySQL('leadsAndClients_db')



@app.route("/")
def home():
    leadsData=mysql.query_db("SELECT label,y FROM customers;")

    return render_template("index.html", jsonData=json.dumps(leadsData),leads_data=leadsData)



if __name__ == "__main__":
    app.run(debug=True)