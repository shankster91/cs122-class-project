'''
This file creates the final dataset for the count of libraries
by zip code. It writes the final dataset to a csv called libraries_zipcode.csv
located in the data folder

The original csv was downloaded from the Institute of Museum and 
Library Services website and converted to a count by zip code
'''

import pandas as pd
import utils

library_raw = pd.read_csv("data/raw_data/pls_fy18_outlet_pud18i.csv")

select_cols = ["ZIP"]

libraries = library_raw.loc[:,select_cols]

count = pd.Series(libraries.squeeze().values.ravel()).value_counts()
lib_count = pd.DataFrame({'zip' : count.index, 'libraries_count' : count.values})

lib_csv = utils.compute_density(lib_count)
lib_csv.fillna(0, inplace=True)

lib_csv.to_csv("data/libraries_zipcode.csv", index=False)
