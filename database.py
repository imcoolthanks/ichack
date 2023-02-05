import sqlite3 as sql
import csv

def get_file(txtFile, company):
    try:
        with open(txtFile) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    if (float(row[0]) not in range(7000, 9000) and 
                        float(row[1]) not in range(8, 10) and 
                        float(row[2]) not in range(20, 30) and 
                        float(row[3]) not in range(40, 100)): 
                        
                        raise Exception(f'Cannot accept data at line {line_count - 1}.')
                    else:
                        line_count += 1
    except Exception as e:
        print(e)
        return ()
    else:                   
        #Create database file/connect to it
        conn = sql.connect("companies.db")

        try:
        #Create table
            query = """CREATE TABLE {name} (raw TEXT, co2 TEXT, imports TEXT, reusable TEXT)""".format(name=company)

            conn.execute(query)

            print("table created")
        except:
            print("Table already exists.")

        #Get all rows from csv file
        with open(txtFile, newline='') as f:
            reader = csv.reader(f)
            next(reader) #skip headers line
            data = list(reader)

        #Connect to database
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

# get_file("validCompanies.csv", "Amazon")
# list_all("Amazon")

def create_logins():
#Create database file/connect to it
        conn = sql.connect("logins.db")
        try:
        #Create table
            query = """CREATE TABLE logins (company TEXT, email TEXT PRIMARY KEY, password TEXT)"""

            conn.execute(query)

            print("table created")
        except:
            print("Table alr existed")

def create_comp_size():
#Create database file/connect to it
        conn = sql.connect("logins.db")
        try:
        #Create table
            query = """CREATE TABLE company_size (company TEXT PRIMARY KEY, company_size int)"""

            conn.execute(query)

            print("table created")
        except:
            print("Table alr existed")

def new_logins(): #Pass in an array of info (email, interest) like this
    #Connect to database
    conn = sql.connect("logins.db")
    cur = conn.cursor()
    
    #Load all rows
    insert_query = """INSERT INTO logins (company, email, password) VALUES (?,?,?)"""
    cur.execute(insert_query, ("Amazon", "amazon@gmail.com", "amazon"))
    cur.execute(insert_query, ("Cisco", "cisco@gmail.com", "cisco"))
    cur.execute(insert_query, ("Palantir", "palantir@gmail.com", "palantir"))
    cur.execute(insert_query, ("HRT", "hrt@gmail.com", "hrt"))

    #Save changes
    conn.commit()

    conn.close()

    print("Loading completed")

def new_comp_size(): #Pass in an array of info (email, interest) like this
    #Connect to database
    conn = sql.connect("logins.db")
    cur = conn.cursor()
    
    #Load all rows
    insert_query = """INSERT INTO company_size (company, company_size) VALUES (?,?)"""
    cur.execute(insert_query, ("Amazon", 150))
    cur.execute(insert_query, ("Cisco", 803))
    cur.execute(insert_query, ("Palantir", 124))
    cur.execute(insert_query, ("HRT", 324))

    #Save changes
    conn.commit()

    conn.close()

    print("Loading completed")

# ---- DEBUGGING ---------
def list_all(): 
    conn = sql.connect("logins.db")
    cur = conn.cursor()

    cur.execute("select * from company_size")
    
    rows = list(cur.fetchall())

    conn.close()

    print(rows)