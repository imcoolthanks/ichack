# run with py -m flask --app="Flask/app.py" run

import os
from flask import Flask, render_template, Response, request, redirect, url_for
from werkzeug.utils import secure_filename
import sqlite3 as sql
import json

app = Flask(__name__)
UPLOAD_FOLDER = ['./csvFiles/']
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

@app.route('/dashboard/<name>/<cat>', methods=["GET"])
def dashboard(name, cat):
    from mlmodel import averages

    def suggestions(company):
        messeges = ['''Your CO2 emissions were higher than average, try to cut down on 
                your emissions for a better rating.''',
                '''Your percentage of foreign imports of materials was higher than 
                average, try to source materials nationally for a better rating.''',
                '''Your percentage of reusable materials was lower than average, 
                try to find more sustainable materials for a better rating.''',
                ''' Your CO2 emissions and percentage of foreign imports were both 
                lower than average, and your percentage of reusable materials was 
                higher than average. You're company is sustainable! Keep it up!''']

        raw, co2, imports, reusables = get_data(company)

        returnmessege = ''

        if (float(co2[0]) < averages[0]) & ((float(imports[0])) < averages[1]) & ((float(reusables[0])) > averages[2]):
            returnmessege = messeges[3]
        if float(co2[0]) > averages[0]:
            returnmessege = messeges[0]
        if float(imports[0]) > averages[1]:
            returnmessege = messeges[1]
        if float(reusables[0]) < averages[2]:
            returnmessege = messeges[2]
        
        return returnmessege

    types = ["raw", "co2", "imports", "reusables", "suggestions"]
    index = str(types.index(cat))
    suggestions = suggestions(name)
    if index == "4": 
        return render_template("dashboard.html", company=name, suggestions=suggestions, graph_url="suggestions", cat = cat)
    else:
        return render_template("dashboard.html", company=name, graph_url='Assets/graphs/'+name+index+".png", cat = cat)

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
            return redirect(url_for('.dashboard', name=company, cat="raw"))
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
  
@app.route('/csv_download', methods=['GET', 'POST'])
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

    plt.plot(years, raw_materials_data)
    plt.scatter(years, raw_materials_data, s = 10, color='black')
    plt.title('Raw materials used in a year')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    plt.ylabel("Tonnes")
    for index in range(len(years)):
        plt.text(years[index], raw_materials_data[index], raw_materials_data[index], size=6)
    save_url = 'Assets/graphs/'+company+'0.png'
    plt.savefig('Flask/static/'+ save_url)

    plt.plot(years, co2_data)
    plt.scatter(years, co2_data, s = 10, color='black')
    plt.title('CO2 emissions')
    plt.xticks(np.arange(min(years), max(years)+1, 10.0))
    plt.ylabel("Mass /g")
    for index in range(len(years)):
        plt.text(years[index], co2_data[index], co2_data[index], size=6)
    save_url = 'Assets/graphs/'+company+'1.png'
    plt.savefig('Flask/static/'+ save_url)

    plt.plot(years, percentage_foreign)
    plt.scatter(years, percentage_foreign, s = 10, color='black')
    plt.title('Percentage of foreign imports of materials')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    plt.ylabel("Mass /g")
    for index in range(len(years)):
        plt.text(years[index], percentage_foreign[index], percentage_foreign[index], size=6)
    save_url = 'Assets/graphs/'+company+'2.png'
    plt.savefig('Flask/static/'+ save_url)

    plt.plot(years, percentage_reusable)
    plt.scatter(years, percentage_reusable, s = 10, color='black')
    plt.title('Percentage of reusable material')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    plt.ylabel("Mass /g")
    for index in range(len(years)):
        plt.text(years[index], percentage_reusable[index], percentage_reusable[index], size=6)
    save_url = 'Assets/graphs/'+company+'3.png'
    plt.savefig('Flask/static/'+ save_url)

