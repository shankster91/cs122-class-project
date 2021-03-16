'''
This file creates the final dataset for the count of museums
by zip code. It writes the final dataset to a csv called museums_zipcode.csv
located in the data folder

The original csvs were downloaded from the Institute of Museum and
Library Services website and are joined together here and converted
to a count by zip code
'''

import pandas as pd
import utils

museums_raw1 = pd.read_csv("data/raw_data/MuseumFile2018_File1_Nulls.csv")
museums_raw2 = pd.read_csv("data/raw_data/MuseumFile2018_File2_Nulls.csv")

select_cols = ["GZIP5"]

museums1 = museums_raw1.loc[:,select_cols]
museums2 = museums_raw2.loc[:,select_cols]

museums = museums1.append(museums2)
museums = pd.to_numeric(museums['GZIP5'], errors="coerce")

count = pd.Series(museums.squeeze().values.ravel()).value_counts()
museums_count = pd.DataFrame({'zip' : count.index, 'museums_count' : count.values})

museums_csv = utils.compute_density(museums_count)
museums_csv.fillna(0, inplace=True)

museums_csv.to_csv("data/museums_zipcode.csv", index=False)
