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
        raw_materials_data.append(float(r[0]))
        co2_data.append(float(r[1]))
        percentage_foreign.append(float(r[2]))
        percentage_reusable.append(float(r[3]))

    return raw_materials_data, co2_data, percentage_foreign, percentage_reusable

def plot(company):
    years = []

    raw_materials_data, co2_data, percentage_foreign, percentage_reusable = get_data(company)

    # get all the years
    current_year = datetime.date.today().year
    for i in range(len(raw_materials_data)):
        years.append(current_year - i)
    years.reverse

    # ----------------------------------------------------------------
    # Raw materials used in a year
    # ----------------------------------------------------------------
    plt.plot(years, raw_materials_data)
    plt.scatter(years, raw_materials_data, s = 10, color='black')
    plt.title('Raw materials used in a year')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    
    plt.ylabel("Tonnes")
    scale = (min(raw_materials_data) - max(raw_materials_data))/2
    plt.gca().set_ylim([min(raw_materials_data) + scale, max(raw_materials_data) - scale])
    
    for index in range(len(years)):
        plt.text(years[index], raw_materials_data[index], raw_materials_data[index], size=6)
    save_url = 'Assets/graphs/'+company+'0.png'
    plt.savefig('Flask/static/'+ save_url)
    
    plt.show()

    # ----------------------------------------------------------------
    # CO2 emissions
    # ----------------------------------------------------------------
    plt.plot(years, co2_data)
    plt.scatter(years, co2_data, s = 10, color='black')
    plt.title('CO2 emissions')
    plt.xticks(np.arange(min(years), max(years)+1, 10.0))
    
    plt.ylabel("Million Tonnes")
    scale = (min(co2_data) - max(co2_data))/2
    plt.gca().set_ylim([min(co2_data) + scale, max(co2_data) - scale])
    
    for index in range(len(years)):
        plt.text(years[index], co2_data[index], co2_data[index], size=6)
    save_url = 'Assets/graphs/'+company+'1.png'
    plt.savefig('Flask/static/'+ save_url)
    
    plt.show()

    # ----------------------------------------------------------------
    # Percentage of foreign imports of materials
    # ----------------------------------------------------------------
    plt.plot(years, percentage_foreign)
    plt.scatter(years, percentage_foreign, s = 10, color='black')
    plt.title('Percentage of foreign imports of materials')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    
    plt.ylabel("Percentage %")
    scale = (min(percentage_foreign) - max(percentage_foreign))/2
    plt.gca().set_ylim([min(percentage_foreign) + scale, max(percentage_foreign) - scale])
    
    for index in range(len(years)):
        plt.text(years[index], percentage_foreign[index], percentage_foreign[index], size=6)
    save_url = 'Assets/graphs/'+company+'2.png'
    plt.savefig('Flask/static/'+ save_url)
    
    plt.show()

    # ----------------------------------------------------------------
    # Percentage of reusable material
    # ----------------------------------------------------------------
    plt.plot(years, percentage_reusable)
    plt.scatter(years, percentage_reusable, s = 10, color='black')
    plt.title('Percentage of reusable material')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    
    plt.ylabel("Percentage %")
    scale = (min(percentage_reusable) - max(percentage_reusable))/2
    plt.gca().set_ylim([min(percentage_reusable) + scale, max(percentage_reusable) - scale])
    
    for index in range(len(years)):
        plt.text(years[index], percentage_reusable[index], percentage_reusable[index], size=6)
    save_url = 'Assets/graphs/'+company+'3.png'
    plt.savefig('Flask/static/'+ save_url)
    
    plt.show()


get_data("Apple")
plot("Apple")