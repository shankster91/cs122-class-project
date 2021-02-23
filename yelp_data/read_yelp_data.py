'''
Read in yelp files
'''

import json
import pandas as pd

filename = "/Users/carolinekinnen/Desktop/yelp_dataset/yelp_academic_dataset_business.json"


# Read data in as string
f = open(filename)
str_file = f.read()

json_lines = []

line = ""
for char in str_file:
    if char == "\n":
        json_lines.append(line)
        json_lines.append("")
        line = ""
    else:
        line += char

json_dict_list = []

for line in json_lines:
    json_accept = json.loads(line)
    json_dict_list.append(json_accept)

# Create Pandas df out of json list

select_cols = ['business_id', 'name', 'address', 'city', 'state', 'postal_code',
       'latitude', 'longitude', 'stars', 'review_count', 'is_open',
       'categories']

states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

business_df = pd.DataFrame(columns = select_cols)

for dict_entry in json_dict_list: 
    business_select = {key: dict_entry[key] for key in select_cols }
    if business_select['state'] in states:
        business_row = pd.DataFrame(business_select, index = [0])
        business_df = business_df.append(business_select, ignore_index = True)


business_df.to_csv("formatted_business_data.csv")