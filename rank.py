import numpy as np
import sqlite3 as sql
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

RAW_WEIGHT = 0.1
CO2_WEIGHT = 0.45
IMPORT_WEIGHT = 0.15
REUSABLE_WEIGHT = 0.2

def rank():
    with open('model.sav', 'rb') as file:
        loaded_model = pickle.load(file)
        data = np.genfromtxt('test/companies.csv', delimiter=",")[1:]
        sizes = get_company_size_to_array()

        df = pd.DataFrame(data, columns = ["raw", "co2", "import", "reusable"])

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

        print(rankings) 
        pd.DataFrame(rankings).to_csv("test/rankings.csv", header = None)

def get_company_size_to_array():
    conn = sql.connect("logins.db")
    cur = conn.cursor()

    cur.execute("select * from company_size")
    rows = np.array(cur.fetchall())
    conn.close()

    return rows

def get_companies_to_array():
    conn = sql.connect("companies.db")
    cur = conn.cursor()

    cur.execute("select * from company_size")
    rows = np.array(cur.fetchall())
    conn.close()

    return rows
