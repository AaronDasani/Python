from flask import Flask,render_template,request,redirect
from databaseConnection import connectToMySQL
import json

app = Flask(__name__)

mysql = connectToMySQL('leadsAndClients_db')


@app.route("/")
def home():

    leadsData=mysql.query_db("SELECT name,lead_amount FROM customers;")
    # print(leadsData)
    
    return render_template("index.html", leads_data=leadsData)






if __name__ == "__main__":
    app.run(debug=True)