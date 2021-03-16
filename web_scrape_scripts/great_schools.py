'''
This file scrapes GreatSchools.org for the average rating of schools
in every zip code in the US. It writes the final dataset to a csv called  
great_schools.csv located in the data folder
'''

import bs4
import requests
import csv
import json
import re
import pandas as pd
import time
       
def get_school_score(zip_code):
    url = "https://www.greatschools.org/search/search.zipcode?sort=rating&view=table&zip=" + str(zip_code)
    req = requests.get(url)

    soup = bs4.BeautifulSoup(req.text, features = 'lxml')

    string = str(soup.find_all("script", type = "text/javascript")[0])

    data_layer = string[string.find('gon.search'):]

    if "Your search did not return any schools in " + str(zip_code) not in data_layer:
        school_string = data_layer.replace('gon.search={"schools":[', "").replace(';\n//]]>\n</script>', "")
        school_list = re.findall(r'"id":.*?"remediationData":', school_string)

        total = 0
        count = 0
        for item in school_list:
            json_school = json.loads("{" + item + "{}}")
            rating = json_school['rating']
            if isinstance(rating, int):
                total += rating
                count += 1
        
        if count != 0:
            return total / count
        else:
            return -1

    else:
        return -1
    
def school_crawl_df(zip_code_list):
    school_rating_list = []
    index = 0
    for zip_code in zip_code_list:
        school_rating = get_school_score(str(zip_code))
        school_rating_list.append(school_rating)
        index += 1

        if index % 100 == 0:
            time.sleep(1)
        #    print("finished zip", zip_code, "at index", index)

    pd_dict = {"zip": zip_code_list, "school_rating": school_rating_list}
    df = pd.DataFrame(pd_dict)

   # return_df.to_csv("data/great_schools.csv", index=False)

    return df

zip_code_list = pd.read_csv("data/census_data.csv").loc[:,"zip"]

return_df = school_crawl_df(zip_code_list[0:100])
print(return_df)


