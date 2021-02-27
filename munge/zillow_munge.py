'''
This file cleans the Zillow data by filtering out the unecessary columns and
renaming the columns of interest.
'''

import pandas as pd


data = pd.read_csv('data/raw_data/zillow.csv')

data.rename(columns = {'ZHVI_3mo' : 'property_value_avg'}, inplace=True)
data = data[['Zip', 'property_value_avg']]

data.to_csv('data/zillow.csv', index=False)
