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
            print("Table alr existed")

        conn.close()
    
def new_company_data(csv_file, company): #Pass in an array of info (email, interest) like this
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

#get_file("companies.csv", "Safari")
# new_company_data("Amazon.db", [80.0, 19.2, 22.23, 73.77])
# list_all("Amazon")

get_file("validCompanies.csv", "Jiawen")
new_company_data("validCompanies.csv", "Jiawen")
list_all("Jiawen")
