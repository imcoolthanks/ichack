# run with py -m flask --app="Flask/app.py" run

from flask import Flask, render_template, Response, request, redirect, url_for
import sqlite3 as sql
import json

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

@app.route('/dashboard/', methods=["GET"])
def dashboard():
    return render_template("dashboard.html", company=request.args.get('name'))

@app.route("/login/", methods = ['POST', 'GET'])
def login():                
    if request.method == 'POST':
        email = request.form.get('email') 
        password = request.form.get('password')

        success, company = _login(email, password)
        
        if success:
            #Does stuff to load the website

            return redirect(url_for('.dashboard', name=company))
        else:
            return render_template('login.html', error="Incorrect email or password.")

    return render_template('login.html')

def _login(email, password):
    conn = sql.connect("logins.db")
    cur = conn.cursor()

    try:
        query = 'SELECT company, password FROM logins WHERE email = ?'
        cur.execute(query, (email,))
        (company, true_password) = cur.fetchall()[0]
    except:
        print("Invalid Email Address.")
        return False

    conn.close()

    if password == true_password:
        print("Logged in")
        return True, company
    else:
        print("Wrong Password")
        return False, ""

@app.route('/setting/')
def setting():
    return render_template("setting.html")
  
@app.route('/csv_download')
def csv_download():
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})