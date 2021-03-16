
import pandas as pd
import utils

library_raw = pd.read_csv("data/raw_data/pls_fy18_outlet_pud18i.csv")

select_cols = ["ZIP"]

libraries = library_raw.loc[:,select_cols]

# get unique addresses

count = pd.Series(libraries.squeeze().values.ravel()).value_counts()
lib_csv = pd.DataFrame({'zip' : count.index, 'libraries_count' : count.values})

lib_csv = utils.compute_density(lib_csv)
lib_csv.fillna(0, inplace=True)

lib_csv.to_csv("data/libraries_zipcode.csv", index=False)
