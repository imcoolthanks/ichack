from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def unloggedin():
    return render_template("unloggedin.html")

@app.route('/home/')
def home():
    return render_template("home.html")

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/login/')
def login():
    return render_template("login.html")

@app.route('/setting/')
def setting():
    return render_template("setting.html")