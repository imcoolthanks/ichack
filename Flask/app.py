# run with py -m flask --app="Flask/app.py" run

import os
from flask import Flask, render_template, Response, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "../Flask/logFiles"
ALLOWED_EXTENSIONS = set(['.csv', '.txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
  
@app.route('/csv_download')
def csv_download():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['../Flask/csvFiles'], filename))
    return redirect("/setting")