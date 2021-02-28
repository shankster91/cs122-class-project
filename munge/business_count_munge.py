'''
Read in txt files from Economic Census Report and join to find 
count of business establishment types in every zip code in America
'''

import pandas as pd

business_detail = pd.read_csv("data/raw_data/zbp18detail_sample.txt", encoding="cp1252", dtype = {'zip': object, "naics": str})
business_codes = pd.read_csv("data/raw_data/naics_codes_2017.txt", encoding="cp1252", dtype = {"NAICS": str})
business_codes.rename(columns = {"NAICS": "naics", "DESCRIPTION": "description"}, inplace = True)

business = business_detail.merge(business_codes, on = "naics")

codes_select = list(business_codes[business_codes["naics"].str.contains("----")][1:]['naics'])
columns_select = ["zip", "est", "description"]

business_detail_select = business[business['naics'].isin(codes_select)].loc[:,columns_select]

business_count = business_detail_select.pivot_table(index = ["zip"], columns = 'description', values = "est").fillna(0)

business_count.to_csv("data/business_count_sample.csv", index=False)

