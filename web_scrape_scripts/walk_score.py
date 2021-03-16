'''
Pull Walk Score by zip
'''

import bs4
import re
import time
import pandas as pd
import util

def get_walk_score(zip_code):

    url = "https://www.walkscore.com/score/" + str(zip_code)
    req = util.get_request(url)
    if req:
        text = util.read_request(req)
    else:
        #print("error zip:", zip_code)
        score =  -1
        text = None
    if text:
        soup = bs4.BeautifulSoup(text, "html5lib")
        span = soup.find('span', attrs = {'id' : 'score-description-sentence'})
        try:
            score_txt = span.text
            match = re.search("(Walk Score of)(\s)(\d+)(\s)", score_txt)
            score = int(match.group(3))
        except AttributeError:
            #print("error zip:", zip_code)
            score = -1
    else:
        #print("error zip:", zip_code)
        score =  -1

    return score

def get_walk_score_lst(zip_list):

    walk_score_lst = []
    index = 0
    for zip_code in zip_list:
        walk_score = get_walk_score(zip_code)
        walk_score_lst.append(walk_score)
        index += 1
    
        if index % 100 == 0:
            time.sleep(2)
            print("Done with zip #", index)
    
    return walk_score_lst

def walk_score_to_csv(zip_list, filename):

    walk_score_lst = get_walk_score_lst(zip_list)
    pd_dict = {'zip': zip_list, 'walk_score': walk_score_lst}
    df = pd.DataFrame(pd_dict)

    #df.to_csv(filename, index = False)
    df.to_csv(filename, index = False, mode = 'a', header = False)