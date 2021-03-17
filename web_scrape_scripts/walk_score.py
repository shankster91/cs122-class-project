'''
This file scrapes walk score by zip code from walkscore.com
'''

import re
import time
import bs4
import pandas as pd
import util

def get_walk_score(zip_code):
    '''
    Gets walk score for single zip code

    Input:
    zip_code (str or int): a US zip code

    Output:
    score (int): Walk score for that zip code. Missing values get -1.
    '''

    url = "https://www.walkscore.com/score/" + str(zip_code)
    req = util.get_request(url)
    if req:
        text = util.read_request(req)
    else:
        score =  -1
        text = None
    if text:
        soup = bs4.BeautifulSoup(text, features = 'lxml')
        span = soup.find('span', attrs = {'id' : 'score-description-sentence'})
        try:
            score_txt = span.text
            match = re.search("(Walk Score of)(\s)(\d+)(\s)", score_txt)
            score = int(match.group(3))
        except AttributeError:
            score = -1
    else:
        score =  -1

    return score

def get_walk_score_lst(zip_list):
    '''
    Takes list of zip codes and returns list of corresponding zip scores

    Input:
    zip_list (list): list of US zip codes

    Output:
    walk_score_lst (list): List of Walk scores for the zip codes.
    '''

    walk_score_lst = []
    index = 0
    for zip_code in zip_list:
        walk_score = get_walk_score(zip_code)
        walk_score_lst.append(walk_score)
        index += 1

        if index % 100 == 0:
            time.sleep(1)
            print("Done with zip #", index)

    return walk_score_lst

def walk_score_to_csv(zip_list, filename):
    '''
    Takes list of zip codes and writes list of corresponding walk scores
    to CSV.

    Input:
    zip_list (list): list of US zip codes
    filename (str): output filename

    Output:
    No return but writes a CSV file with zip codes and walk scores.
    '''

    walk_score_lst = get_walk_score_lst(zip_list)
    pd_dict = {'zip': zip_list, 'walk_score': walk_score_lst}
    df = pd.DataFrame(pd_dict)

    df.to_csv(filename, index = False, mode = 'a', header = False)

# Command line func for purpose of showing how script works
if __name__ == "__main__":
    cl_zip_list = pd.read_csv("data/census_data.csv").loc[:,"zip"].to_list()
    cl_walk_score_lst = get_walk_score_lst(cl_zip_list[:100])
    cl_pd_dict = {'zip': cl_zip_list[:100], 'walk_score': cl_walk_score_lst}
    cl_df = pd.DataFrame(cl_pd_dict)

    print(cl_df)
