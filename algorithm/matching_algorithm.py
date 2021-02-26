'''
This file contains the algorithm that computes the sum of squared differences
between the attributes of a user-specified zip code and the attributes of each
zip code in a user-specified state. The algorithm then selects the five zip
codes in that state that are most similar to the user-specified zip code
(i.e. it selects the five zip codes with the smallest sum of squared differences).
'''

import math
import sqlite3


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
                  JOIN ideology AS i ON i.zip = c.zip
                  JOIN libraries AS l ON l.zip = c.zip
                  JOIN museums AS m ON m.zip = c.zip
                  JOIN walk_score AS w ON w.zip = c.zip
                  JOIN zillow AS z ON z.zip = c.zip
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
    conn = sqlite3.connect('../zip_db.sqlite3')
    sql_query, args = create_sql_query(args_from_ui['state'], args_from_ui['zip'])
    cursor = conn.cursor()
    r = cursor.execute(sql_query, args)
    zip_data = r.fetchall()
    # header = get_header(cursor)
    conn.close()

    # separate data in zip_data and start_zip_data, eliminate the specifid zip code from the output list
    # group variables by table?
    # find best zips, with weights on diff aspects
    return zip_data # edit return value



# libraries to counts--and zero counts
# museums to counts--and zero counts
# business_counts zero counts
# try two types of searches (zip is not in specified state and zip is in specified state)
# check size of joined dataset
# del duplicate columns

# add new census data to db
# pylint, git, close ssh
