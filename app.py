from flask import Flask, render_template, request, session, Response
import json

app = Flask(__name__)
with app.open_resource("secret/secretkey.txt",'r') as f:
    app.config['SECRET_KEY'] = f.read()

with app.open_resource("codes.json", 'r') as f:
    codes = json.load(f)

currentUnit = 0.0

def validateCode(code) -> bool:
    if code.lower() in codes.keys():
        session['role'] = codes[code.lower()]
        return True
    else:
        return False

@app.route("/", methods = ["GET", "POST"])
def homePage():
    if request.method == "POST":
        roomCode = request.form["roomCode"]
        if validateCode(roomCode):
            if session['role'] == "teacher":
                return render_template("tableofcontents.html", value=getValue())
            else:
                return render_template(str(currentUnit) + ".html", value=getValue())
    return render_template("home.html")

@app.route("/<float:v>", methods = ["GET"])
def unit1Page(v):
    global currentUnit
    if session['role'] == "teacher":
        currentUnit = v
    return render_template(str(currentUnit) + ".html", value=getValue())

@app.route("/getunit")
def getUnit():
    return Response(str(currentUnit), mimetype="text/plain")

@app.errorhandler(404)
def nullPage(error):
    return "<link rel='stylesheet' type='text/css' href='static/unitIntro.css'><body><div id='gradientbackground'></div><div id='starbackground'></div><div class='center'><p class='unitText' id='description'>uh oh</p></div></body>"

def getValue():
    return {"currentUnit":currentUnit}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
