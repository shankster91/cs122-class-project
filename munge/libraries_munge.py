
import pandas as pd 

library_raw = pd.read_csv("data/raw_data/pls_fy18_outlet_pud18i.csv")

select_cols = ["ZIP"]

libraries = library_raw.loc[:,select_cols]

# get unique addresses

count = pd.Series(libraries.squeeze().values.ravel()).value_counts()
libraries_csv = pd.DataFrame({'libraries_zip': count.index, 'libraries_count':count.values})

libraries_csv.to_csv("data/libraries_zipcode.csv")