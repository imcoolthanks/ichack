# run with py -m flask --app="Flask/app.py" run

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def unloggedin():
    return render_template("unloggedin.html")
  
@app.route('/aboutus/')
def about_us():
  return render_template("about_us.html")

@app.route('/benefits/')
def benefits():
  return render_template("benefits.html")

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/setting/')
def setting():
    return render_template("setting.html")