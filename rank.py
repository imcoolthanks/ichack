import numpy as np
import sqlite3 as sql
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

RAW_WEIGHT = 0.1
CO2_WEIGHT = 0.45
IMPORT_WEIGHT = 0.15
REUSABLE_WEIGHT = 0.2


def get_companies_to_array():
    conn = sql.connect("companies.db")
    cur = conn.cursor()

    # get all tables
    cur.execute("""SELECT name FROM sqlite_master  
    WHERE type='table';""")
    companies = []
    company_data = []
    company_size_data = []

    for i in list(cur.fetchall()):
        companies.append(i[0])

    try:
        companies.remove("company_size")
        companies.remove("rank")
    except:
        print("companies_size or rank exist")

    for comp in companies:
        cur.execute("""SELECT raw, co2, imports, reusable FROM """ + comp)
        comp_rows = list(cur.fetchall())[0]
        cur.execute("select company_size from company_size where company = '"+ comp +"'")
        company_size = list(cur.fetchall())[0][0]
        company_data.append(comp_rows)
        company_size_data.append(company_size)

    return companies, np.array(company_data), np.array(company_size_data)

def rank():
    with open('model.sav', 'rb') as file:
        loaded_model = pickle.load(file)
        companies, data, sizes = get_companies_to_array()

        df = pd.DataFrame(data, columns = ["raw", "co2", "import", "reusable"])

        df["raw"] = pd.to_numeric(df["raw"])
        df["co2"] = pd.to_numeric(df["co2"])
        df["import"] = pd.to_numeric(df["import"])
        df["reusable"] = pd.to_numeric(df["reusable"])

        df['raw'] = df['raw'].apply(lambda x: x * RAW_WEIGHT)
        df['co2'] = df['co2'].apply(lambda x: x* CO2_WEIGHT) 
        df['import'] = df['import'].apply(lambda x: x * IMPORT_WEIGHT)
        df['reusable'] = df['reusable'].apply(lambda x: x * REUSABLE_WEIGHT)

        scaler = StandardScaler()
        standardized_data = scaler.fit_transform(df)
        standardized_df = pd.DataFrame(standardized_data, columns=df.columns)
        df = standardized_df
        
        df['co2'] = df['co2'].apply(lambda x: x* -1) 
        df['import'] = df['import'].apply(lambda x: x * -1)

        r = len(df.index)
        for i in range(r):
            df['co2'].iloc[i] /= sizes[i]
            df['raw'].iloc[i] /= sizes[i]

        data = df.to_numpy()
        rankings = loaded_model.predict(data)

        print(companies, rankings)

        inserts = list(zip(companies, rankings))

        return inserts

def create_table(inserts):
    print(inserts)
    # Load ranking into csv
    conn = sql.connect("companies.db")
    cur = conn.cursor()

    try:
        query = """CREATE TABLE rank (company TEXT PRIMARY KEY, rank TEXT)"""
        conn.execute(query)
    except:
        print("table exist")
    
    #Load all rows
    for i in inserts:
        insert_query = """INSERT INTO rank (company, rank) VALUES (?,?)"""
        cur.execute(insert_query, (i[0], i[1]))

    #Save changes
    conn.commit()

    conn.close()

# ---- DEBUGGING ---------
def list_all(): 
    conn = sql.connect("companies.db")
    cur = conn.cursor()

    cur.execute("select * from rank")
    
    rows = list(cur.fetchall())

    conn.close()

    print(rows)

create_table(rank())
list_all()