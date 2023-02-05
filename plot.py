import math
import numpy as np
from matplotlib import pyplot as plt
import csv
import datetime

import sqlite3 as sql

# Line graphs
# - Raw materials used in a year
# - CO2 emissions
# - Percentage of foreign imports of materials
# - Percentage of reusable material

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