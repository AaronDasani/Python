from flask import Flask,render_template
app=Flask(__name__)

@app.route("/")
def index():
    return ("Type '/play' in the address bar")

@app.route("/play")

def play():
    
    return render_template("index.html", greet="Welcome!",amount=3)

@app.route("/play/(<x>)")

def play_x(x):

    return render_template("index.html", greet="Welcome!",amount=int(x))

@app.route("/play/(<x>)/(<color>)")

def box_color(x,color):
    
    return render_template("index.html", greet="Welcome!",amount=int(x),boxColor=color)


if __name__=="__main__":
    app.run(debug=True)