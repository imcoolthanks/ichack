import math
import numpy as np
from matplotlib import pyplot as plt

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
    current_year = 2023
    for i in range(len(raw_materials_data)):
        years.append(current_year - i)
    years.reverse

    #Plotting data
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(8,8))

    fig.suptitle('Sustainablity of ' + company)

    ax1.plot(years, raw_materials_data)
    ax1.title.set_text('Raw materials used in a year')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    ax1.set_ylabel("Tonnes")


    ax2.plot(years, co2_data)
    ax2.title.set_text('CO2 emissions')
    plt.xticks(np.arange(min(years), max(years)+1, 10.0))
    ax2.set_ylabel("Mass /g")

    ax3.plot(years, percentage_foreign)
    ax3.title.set_text('Percentage of foreign imports of materials')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    ax3.set_ylabel("Mass /g")

    ax4.plot(years, percentage_reusable)
    ax4.title.set_text('Percentage of reusable material')
    plt.xticks(np.arange(min(years), max(years)+1, 1.0))
    ax4.set_ylabel("Mass /g")

    fig.tight_layout()

    plt.show()

plot("Amazon")