# run with py -m flask --app="Flask/app.py" run

import os
from flask import Flask, render_template, Response, request, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3 as sql


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
    name = request.args.get('name')
    return render_template("dashboard.html", company=name, graph_url='Assets/graphs/' + name + ".png")

@app.route("/login/", methods = ['POST', 'GET'])
def login():                
    if request.method == 'POST':
        email = request.form.get('email') 
        password = request.form.get('password')

        #DELETE
        email = "amazon@gmail.com"
        password = "amazon"

        success, company = _login(email, password)
        
        if success:
            #Does stuff to load the website
            graph(company)
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

def graph(company):
    print("Graphing")
    get_data(company)
    plot(company)

@app.route('/setting/')
def setting():
    return render_template("setting.html")
  
@app.route('/csv_download')
def csv_download():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['../Flask/csvFiles'], filename))
    return redirect("/setting")

import numpy as np
from matplotlib import pyplot as plt
import datetime
import sqlite3 as sql


def get_data(company):
    raw_materials_data = []
    co2_data = []
    percentage_foreign = []
    percentage_reusable = []
        
    conn = sql.connect("companies.db")
    cur = conn.cursor()

    cur.execute("select * from " + company)
    
    rows = list(cur.fetchall())

    conn.close()

    for r in rows:
        raw_materials_data.append(r[0])
        co2_data.append(r[1])
        percentage_foreign.append(r[2])
        percentage_reusable.append(r[3])

    return raw_materials_data, co2_data, percentage_foreign, percentage_reusable

def plot(company):
    years = []

    raw_materials_data, co2_data, percentage_foreign, percentage_reusable = get_data(company)

    # get all the years
    current_year = datetime.date.today().year
    for i in range(len(raw_materials_data)):
        years.append(current_year - i)
    years.reverse

    #Plotting data
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8,8))

    fig.suptitle('Sustainablity of ' + company)

    ax1.plot(years, raw_materials_data)
    ax1.scatter(years, raw_materials_data, s = 10, color='black')
    ax1.title.set_text('Raw materials used in a year')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    ax1.set_ylabel("Tonnes")
    for index in range(len(years)):
        ax1.text(years[index], raw_materials_data[index], raw_materials_data[index], size=6)


    ax2.plot(years, co2_data)
    ax2.scatter(years, co2_data, s = 10, color='black')
    ax2.title.set_text('CO2 emissions')
    plt.xticks(np.arange(min(years), max(years)+1, 10.0))
    ax2.set_ylabel("Mass /g")
    for index in range(len(years)):
        ax2.text(years[index], co2_data[index], co2_data[index], size=6)

    ax3.plot(years, percentage_foreign)
    ax3.scatter(years, percentage_foreign, s = 10, color='black')
    ax3.title.set_text('Percentage of foreign imports of materials')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    ax3.set_ylabel("Mass /g")
    for index in range(len(years)):
        ax3.text(years[index], percentage_foreign[index], percentage_foreign[index], size=6)

    ax4.plot(years, percentage_reusable)
    ax4.scatter(years, percentage_reusable, s = 10, color='black')
    ax4.title.set_text('Percentage of reusable material')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    ax4.set_ylabel("Mass /g")
    for index in range(len(years)):
        ax4.text(years[index], percentage_reusable[index], percentage_reusable[index], size=6)

    fig.tight_layout()

    #Save Graph
    save_url = 'Assets/graphs/'+company+'.png'
    plt.savefig('Flask/static/'+ save_url)