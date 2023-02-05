import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import random

companies = []

for i in range(10): 
    # raw average = 8852 
    raw = round(random.uniform(7000, 9000), 6) 
    #co2 average = 8,196,721.31147541
    co2Million = round(random.uniform(8, 10), 6)
    impManufacturing = round(random.uniform(20, 30), 6)
    reusable = round(random.uniform(40, 100), 6)
    companies.append([raw, co2Million, impManufacturing, reusable])

df = pd.DataFrame(companies, columns = ["raw", "co2", "import", "reusable"])

scaler = StandardScaler()
standardized_data = scaler.fit_transform(df)
standardized_df = pd.DataFrame(standardized_data, columns=df.columns)

df = standardized_df

# Sort the data 
# if co2 or foreign is high then negative score
df['co2'] = df['co2'].apply(lambda x: x*-1)
df['import'] = df['import'].apply(lambda x: x*-1)

df['Total'] = df[list(df.columns)].sum(axis=1)
df = df.sort_values(by=['Total'], ascending = True)
df = df.drop(columns=['Total'])

#Give a ranking
block = len(df.index)/5
df['RowNumber'] = np.arange(1, len(df)+1, 1)

ratings = ['A', 'B', 'C', 'D', 'E']

# create a list of our conditions
conditions = [
    (df['RowNumber'] <= block),
    (df['RowNumber'] > block) & (df['RowNumber'] <= block*2),
    (df['RowNumber'] > block*2) & (df['RowNumber'] <= block*3),
    (df['RowNumber'] > block*3) & (df['RowNumber'] <= block*4),
    (df['RowNumber'] > block*4) & (df['RowNumber'] <= block*5)
    ]

# create a new column and use np.select to assign values to it using our lists as arguments
df['Rating'] = np.select(conditions, ratings)
df = df.drop(columns=['RowNumber'])

print(df)


        



