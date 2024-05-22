from flask import Flask, render_template, request, session, Response
import json

# Create a flask object, which will manage the entire server side
app = Flask(__name__)

# Import the secret key from the uncommited file (.gitignore-ed)
with app.open_resource("secret/secretkey.txt",'r') as f:
    app.config['SECRET_KEY'] = f.read()

# Access premade codes for student and teacher side assignment (possibility for expansion)
with app.open_resource("codes.json", 'r') as f:
    codes = json.load(f)

# The global current unit for the only current session (possibility for expansion)
currentUnit = 0.0

# Assign the user's role to be a teacher or student, based on the code given, return True if successful, False if code was not found
# Would be changed in expansion
def validateCode(code) -> bool:
    if code.lower() in codes.keys():
        session['role'] = codes[code.lower()]
        return True
    else:
        return False

# home page, returns home.html by default, changes behavior based on role
@app.route("/", methods = ["GET", "POST"])
def homePage():
    if request.method == "POST":
        roomCode = request.form["roomCode"]
        # When a code is input, validate it, if it was successful move onto either the table of contents (teacher), or the current unit (student)
        if validateCode(roomCode):
            if session['role'] == "teacher":
                return render_template("tableofcontents.html", value=getValue())
            else:
                return render_template(str(currentUnit) + ".html", value=getValue())
    return render_template("home.html")

# any url route that is a float value off the base route
# if the user is a teacher, the global current unit is set to the same page
# if the user is a student, they are sent to the global current unit, allowing the teacher control over what page the student sees
@app.route("/<float:v>", methods = ["GET"])
def unit1Page(v):
    global currentUnit
    if session['role'] == "teacher":
        currentUnit = v
    return render_template(str(currentUnit) + ".html", value=getValue())

# data url, returns the current unit, so that student sides can update themselves
@app.route("/getunit")
def getUnit():
    return Response(str(currentUnit), mimetype="text/plain")

# any invalid route
@app.errorhandler(404)
def nullPage(error):
    return "<link rel='stylesheet' type='text/css' href='static/unitIntro.css'><body><div id='gradientbackground'></div><div id='starbackground'></div><div class='center'><p class='unitText' id='description'>uh oh</p></div></body>"

# general data package sent to html pages
def getValue():
    return {"currentUnit":currentUnit}

# starts the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
