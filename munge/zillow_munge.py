'''
This file cleans the Zillow data by filtering out the unecessary columns and
renaming the columns of interest.
'''

import pandas as pd


data = pd.read_csv('data/raw_data/zillow.csv')

new_names = {'Zip' : 'zip', 'ZHVI_3mo' : 'property_value_avg'}
data.rename(columns = new_names, inplace=True)
data = data[['zip', 'property_value_avg']]

data.to_csv('data/zillow.csv', index=False)
