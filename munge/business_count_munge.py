import pandas as pd

business_detail = pd.read_csv("data/raw_data/zbp18detail.txt", encoding="cp1252")
business_codes = pd.read_csv("data/raw_data/naics_codes_2017.txt", encoding="cp1252")
business_codes.rename(columns = {"NAICS": "naics", "DESCRIPTION": "description"}, inplace = True)
business = business_detail.join(business_codes, on = "naics")

codes_select = list(business_codes[business_codes["naics"].str.contains("----")][1:]['naics'])

business_detail_select = business[business['naics'].isin(codes_select)]


