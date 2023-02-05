import sqlite3 as sql
import csv

def create_company(company):
    #Create database file/connect to it
    conn = sql.connect("companies.db")
    try:
    #Create table
        query = """CREATE TABLE {name} (raw TEXT, co2 TEXT, imports TEXT, reusable TEXT)""".format(name=company)

        conn.execute(query)

        print("table created")
    except:
        print("Table alr existed")

    conn.close()

def new_company_data(csv_file, company, row): #Pass in an array of info (email, interest) like this
    #Get all rows from csv file
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        next(reader) #skip headers line
        data = list(reader)

    #Connect to database
    conn = sql.connect("companies.db")
    cur = conn.cursor()
    
    for row in data:
        #Load all rows
        insert_query = "INSERT INTO " + company + """ (raw, co2,
                                                    imports, reusable) VALUES (?,?,?,?)"""
        cur.execute(insert_query, (row[0], row[1], row[2], row[3]))

    #Save changes
    conn.commit()

    conn.close()

    print("Loading completed")

# ---- DEBUGGING ---------
def list_all(company): 
    conn = sql.connect("companies.db")
    cur = conn.cursor()

    cur.execute("select * from " + company)
    
    rows = list(cur.fetchall())

    conn.close()

    print(rows)
# -------------------------

# create_company("Amazon")
new_company_data("Amazon", [80.0, 19.2, 22.23, 73.77])
list_all("Amazon")

