'''
This file contains the algorithm that computes the sum of squared differences
between the attributes of a user-specified zip code and the attributes of each
zip code in a user-specified state. The algorithm then selects the five zip
codes in that state that are most similar to the user-specified zip code
(i.e. it selects the five zip codes with the smallest sum of squared differences).
'''

import math
import sqlite3
import pandas as pd


def create_sql_query(state, zip_code):
    '''
    Create the SQL query given a user-specified state and a user-specified zip
    code.

    Inputs:
        state: a string representing the postal abbreviation for a U.S. state
        zip_code: an integer representing a U.S. zip code
    
    Outputs:
        A tuple containing 1) a string representing a SQL query, and 2) a tuple
          containing the query's arguments.
    '''
    sql_query = '''SELECT * 
                  FROM census AS c
                  JOIN business_count AS b ON b.zip = c.zip
                  JOIN great_schools AS g on g.zip = c.zip
                  JOIN ideology AS i ON i.zip = c.zip
                  JOIN libraries AS l ON l.zip = c.zip
                  JOIN museums AS m ON m.zip = c.zip
                  JOIN walk_score AS w ON w.zip = c.zip
                  WHERE c.state = ?
                  OR c.zip = ?;'''
    arg_lst = (state, zip_code)
    return (sql_query, arg_lst)


def find_best_zips(args_from_ui):
    '''
    Given user-specified inputs, pull the relevant data and determine the top
    five best zip codes matches.

    Inputs:
        args_from_ui: a dictionary containing the user-specified inputs.
    
    Outputs:
        best_zips: A list of five tuples containing 1) a string representing a
          zip code, and 2) the similarity score corresponding to that zip code.
    '''
    if (not args_from_ui) or ('zip' not in args_from_ui) or \
        ('state' not in args_from_ui):
        return [(None, math.inf)] * 5
    # add assert statement like in PA3?

    state = args_from_ui['state']
    zip_code = args_from_ui['zip']

    conn = sqlite3.connect('../zip_db.sqlite3')
    sql_query, args = create_sql_query(state, zip_code)
    data = pd.read_sql_query(sql_query, conn, params=args)
    conn.close()

    data = data.loc[:, ~data.columns.duplicated()] # maybe there's a better way to do this?
    data.drop('state', axis=1, inplace=True) # warning
    data = data.apply(pd.to_numeric)
    start_zip_data = data[data['zip'] == zip_code] # put this in the class?
    zip_data = data[data['zip'] != zip_code] # put this in the class?

    # find best zips, with weights on diff aspects, average across dist, average across table, deal with nas
    return data # edit return value



#JOIN zillow AS z ON z.zip = c.zip

# add table names (biz counts), add zero counts, density
# delete string variables from Zillow data
# test (2)
# pylint (2)
# update db (2 + census)

# try two types of searches (zip is not in specified state and zip is in specified state)
# check size of joined dataset
# del duplicate columns

# pylint, git, close ssh
