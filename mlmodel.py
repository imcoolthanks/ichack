import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import random
import pickle

RAW_WEIGHT = 0.1
CO2_WEIGHT = 0.45
IMPORT_WEIGHT = 0.15
REUSABLE_WEIGHT = 0.2

def generate_dummy_df():
        companies = []

        for i in range(1000000): 
                raw = round(random.uniform(7000, 9000), 6)
                co2Million = round(random.uniform(8, 10), 6)
                impManufacturing = round(random.uniform(20, 30), 6)
                reusable = round(random.uniform(40, 100), 6)
                companySize = round(random.uniform(1, 1000), 6)
                companies.append([raw * RAW_WEIGHT / companySize,
                co2Million * CO2_WEIGHT / companySize,
                impManufacturing * IMPORT_WEIGHT,
                reusable * REUSABLE_WEIGHT])

        df = pd.DataFrame(companies, columns 
        = ["raw", "co2", "import", "reusable"])

        scaler = StandardScaler()
        standardized_data = scaler.fit_transform(df)
        standardized_df = pd.DataFrame(standardized_data, columns=df.columns)

        df = standardized_df

        # Sort the data 
        # if co2 or foreign is high then negative score
        df['co2'] = df['co2'].apply(lambda x: x*-1)
        df['import'] = df['import'].apply(lambda x: x*-1)

        # Added up all columns for a total score
        df['Total'] = df[list(df.columns)].sum(axis=1)
        df = df.sort_values(by=['Total'], ascending = True)
        df = df.reset_index(drop=True)
        df = df.drop(columns=['Total'])

        #Give a ranking
        block = len(df.index)/5
        df['RowNumber'] = np.arange(1, len(df)+1, 1)

        ratings = ['E', 'D', 'C', 'B', 'A']

        # create a list of our conditions
        conditions = [
                (df['RowNumber'] <= block),
                (df['RowNumber'] > block) & (df['RowNumber'] <= block*2),
                (df['RowNumber'] > block*2) & (df['RowNumber'] <= block*3),
                (df['RowNumber'] > block*3) & (df['RowNumber'] <= block*4),
                (df['RowNumber'] > block*4) & (df['RowNumber'] <= block*5)
        ]

        # create a new column and use np.select to assign values to it
        #  using our lists as arguments
        df['Rating'] = np.select(conditions, ratings)
        df = df.drop(columns=['RowNumber'])

        return df

# Generate the data using the function
data = generate_dummy_df()

# Reorder the data in A,B,C,D,E ...
indexes = []
print(int(len(data)/5))
for i in range(int(len(data)/5)):
        for j in range(0,5):
                indexes.append(i + j*int(len(data)/5))
data = data.reindex(indexes)

print(data)

# Organize our data and split the data
label_names = data['Rating']

# Split the data into training and testing sets
X = data[['raw', 'co2', 'import', 'reusable']]
y = data['Rating']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the model
model = LogisticRegression(multi_class='auto', solver='lbfgs')
model.fit(X_train.values, y_train)
print(X_train)
print("This is X test:")
print(X_test)
print(y_test)

# Evaluate the model on the test data
score = model.score(X_test.values, y_test)
print("Accuracy:", score)

with open('model.sav', 'wb') as file:
        pickle.dump(model, file)