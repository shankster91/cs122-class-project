'''
This file contains the algorithm that computes the average squared difference
between the attributes of a user-specified zip code and the attributes of each
zip code in a user-specified state. The algorithm then selects the five zip
codes in that state that are most similar to the user-specified zip code (i.e.
it selects the five zip codes with the smallest average squared difference).
'''

import re
import math
import sqlite3
import json
import pandas as pd
import numpy as np


class zipInfo(object):
    '''
    Class for representing zip-code-level data and for keeing track of the zip
      codes that are most siliar to the user-specified zip code.
    '''

    def __init__(self, args_from_ui):
        '''
        Construct a data structure to hold the zip-code-level data
        and to keep track of the most similar zip codes.

        Inputs:
            args_from_ui: a dictionary containing the user-specified inputs.
        '''
        data = pull_data(args_from_ui)
        start_zip = args_from_ui['zip']

        self.col_names = data.columns
        self.start_zip_data = data[data['zip'] == start_zip]
        self.data = data[data['zip'] != start_zip]
        self.best_zips = [(None, math.inf)] * 5

        self.table_counts = get_counts('algorithm/table_counts.txt')
        if 'census' in tables:
            self.census_dist_counts = get_counts('algorithm/census_dist_counts.txt')


def pull_data(args_from_ui):
    '''
    Pull zip-code-level data for the starting zip code and for all zip codes in
      the user-specified state.

    Inputs:
        args_from_ui: a dictionary containing the user-specified inputs

    Outputs:
        A pandas dataframe.
    '''
    conn = sqlite3.connect('zip_db.sqlite3')
    sql_query, args = create_sql_query(args_from_ui)
    data = pd.read_sql(sql_query, conn, params=args)
    conn.close()

    data = data.loc[:, ~data.columns.duplicated()] # don't call columns twice?
    data.drop('state', axis=1, errors='ignore', inplace=True)
    data = data.astype(dtype=float)
    data[data.lt(0)] = np.nan
    data = data[(data.drop('zip', axis=1).notnull()).any(axis=1)]

    zips = data['zip']
    data.drop('zip', axis=1, inplace=True) # warning
    data = (data - data.mean())/data.std() # normalize

    return pd.concat([zips, data], axis=1)


def create_sql_query(args_from_ui):
    '''
    Create the SQL query given user-specified parameters.

    Inputs:
        args_from_ui: a dictionary containing the user-specified inputs
    
    Outputs:
        A tuple containing 1) a string representing a SQL query, and 2) a tuple
          containing the query's arguments.
    '''
    state = args_from_ui['state']
    start_zip = args_from_ui['zip'] # don't do this twice?
    table_lst = args_from_ui['tables']

    var_name_lst = []
    join_statement = ''
    for table in table_lst:
        var_name_lst.append(''.join([table, '.*']))
        join_statement = ' '.join([join_statement, 'JOIN', table, 'USING (zip)'])
    var_names = ', '.join(var_name_lst)
    preamble = ' '.join(['SELECT', var_names, 'FROM census AS c'])
    conditions = 'WHERE c.state = ? OR c.zip = ?;'

    sql_query = ' '.join([preamble, join_statement, conditions])
    args = (state, start_zip)

    return (sql_query, args)


def compute_sq_diff(row, zip_info):
    '''
    INSERT HEADER
    '''
    col_names = zip_info.columns
    start_zip_data = zip_info.start_zip_data
    census_dist_counts = zip_info.census_dist_counts
    total_sq_diff = 0
    for col in col_names:
        if col != 'zip':
            table = col.split('_')[0]
            n_vars = zip_info.table_counts[table]
            if table == 'census':
                for var in census_dist_counts:
                    if re.search(var, col):
                        n_bins = census_dist_counts[var]
            sq_diff = (row[col] - start_zip_data[col]) ** 2
            total_sq_diff = np.nansum([total_sq_diff, sq_diff / n_vars])


def get_counts(filename):
    '''
    Takes in the name of a text file containing counts and returns the contents
    of that file in dictionary format.

    Inputs:
        filename: a string representing the name of a text file.

    Outputs:
        A dictionary
    '''
    with open(filename) as f: 
        counts = f.read() 
    return json.loads(counts)


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
    tables = args_from_ui['tables']
    if not tables:
        return 'Please check at least one of the checkboxes.'
    # add assert statement like in PA3?

    zip_info = zipInfo(args_from_ui)

    if zip_info.start_zip_data.empty:
        return 'The specified zip code is not a valid zip code. Please input ' \
               'a valid zip code.'
    if zip_info.data.empty:
        return 'The specified state is not a valid state. Please input a ' \
               'valid state postal abbreviation.'



    zip_info.data.apply(compute_sq_diffs(zip_info))
    #for zip_code, row in zip_info.data.iterrows(): # use apply instead!
    #    zip_info.compute_sq_diff(row)
    # Change denom of average with NAs

    return zip_info.data
    #return start_zip_info.best_zips



# args_from_ui = {'state' : 'OH', 'zip' : 60637, 'tables' : ['census', 'business_count', 'great_schools', 'ideology', 'libraries', 'museums', 'walk_score', 'weather', 'zillow']}

# in orig algorithm, scale all variables to normalize, change denom of 88 to 23, add pop density
# use apply instead of loops, use itertuples for dfs and iteritems for series
# look at comments

# pylint, git, close ssh


    def compute_sq_diff_old(self, zip_data):
        '''
        Compute the average squared difference between the set of attributes for
        two zip codes. Update the zip_selector in place with the best zip code
        matches (i.e. the zip codes that have the smallest average squared
        difference).

        Inputs:
            zip_data: a pandas dataframe containing demographic data for a
              specific zip code.

        Output:
            None
        '''
        _, best5_sq_diff = self.best_zips[4] # average squared diff for the 5th best zip code
        _, best4_sq_diff = self.best_zips[3] # average squared diff for the 4th best zip code
        _, best3_sq_diff = self.best_zips[2] # average squared diff for the 3rd best zip code
        _, best2_sq_diff = self.best_zips[1] # average squared diff for the 2nd best zip code
        _, best1_sq_diff = self.best_zips[0] # average squared diff for the 1st best zip code
        sq_diff = 0
        start_zip_data = self.data.squeeze()
        zip_data = zip_data.squeeze()
        for col in zip_data.index:
            #else:
            #    n = 1
            if re.search('size', col):
                sq_diff += ((zip_data[col] - start_zip_data[col]) * 5.5310) ** 2 / (22 * n) # normalize to put the difference in HH size on a scale of 0 to 100 (5.5310 = 100 / (highest mean HH size - lowest mean HH size))
            else:
                sq_diff += (zip_data[col] - start_zip_data[col]) ** 2 / (22 * n)
            if sq_diff >= best5_sq_diff:
                return None
        if sq_diff >= best4_sq_diff:
            index = 4
        elif sq_diff >= best3_sq_diff:
            index = 3
        elif sq_diff >= best2_sq_diff:
            index = 2
        elif sq_diff >= best1_sq_diff:
            index = 1
        else:
            index = 0
        self.best_zips.pop()
        self.best_zips.insert(index, (zip_data.name, sq_diff))