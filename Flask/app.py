# run with py -m flask --app="Flask/app.py" run

from flask import Flask, render_template, Response

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
    # with open("outputs/Adjacency.csv") as fp:
    #     csv = fp.read()
    csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})