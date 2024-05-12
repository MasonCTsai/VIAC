from flask import Flask, render_template, request, session
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"

with app.open_resource("codes.json", 'r') as f:
    codes = json.load(f)

currentUnit = 0.0

def validateCode(code) -> bool:
    if code in codes.keys():
        session['role'] = codes[code]
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

@app.route("/<float:v>")
def unit1Page(v):
    global currentUnit
    currentUnit = v
    return render_template(str(currentUnit) + ".html", value=getValue())

@app.errorhandler(404)
def nullPage(error):
    return "<p>uh oh</p>"

def getValue():
    return {"currentUnit":currentUnit}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
