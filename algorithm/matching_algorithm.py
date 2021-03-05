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
from scipy import stats


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
        start_zip = args_from_ui['input_zip']
        self.tables = args_from_ui['tables']

        self.col_names = data.columns
        self.start_zip_data = data[data['zip'] == start_zip]
        self.data = data[data['zip'] != start_zip]
        self.best_zips = [(None, math.inf)] * 5


    def compute_sq_diffs(self):
        '''
        Loop through all of the zip codes to compute the average squared
        difference between the attributes of that zip code and the starting zip
        code. Update the zipInfo object in place with the best zip code matches
        (i.e. the zip codes that have the smallest average squared difference).

        Inputs:
            None

        Outputs:
            None
        '''
        col_names = self.col_names
        data = self.data
        start_zip_data = self.start_zip_data
        table_counts = get_counts('algorithm/table_counts.txt')
        if 'census' in self.tables:
            census_dist_counts = get_counts('algorithm/census_dist_counts.txt')
        cols_w_one_var = ('school', 'zillow', 'walk_score')

        for _, row in data.iterrows(): # more efficient method?
            _, best_avg_sq_diff5 = self.best_zips[4] # average squared diff for the 5th best zip code
            _, best_avg_sq_diff4 = self.best_zips[3] # average squared diff for the 4th best zip code
            _, best_avg_sq_diff3 = self.best_zips[2] # average squared diff for the 3rd best zip code
            _, best_avg_sq_diff2 = self.best_zips[1] # average squared diff for the 2nd best zip code
            _, best_avg_sq_diff1 = self.best_zips[0] # average squared diff for the 1st best zip code
    
            # Adjust the number of variables and tables to take into account the
            # presence of NANs.
            # Weather is the only table that can have NANs for some variables both not
            # others. Therefore, we need to count the number of NANs in the weather table.
            num_tables = len(self.tables)
            num_weather_vars = table_counts['weather']
            for col in col_names: # maybe don't loop twice?
                if col.startswith(cols_w_one_var) or col == 'votes_dem':
                    if np.isnan(row[col] - start_zip_data[col].values[0]):
                        num_tables -= 1
                elif col.startswith('weather'):
                    if np.isnan(row[col] - start_zip_data[col].values[0]):
                        num_weather_vars -= 1
            if num_weather_vars == 0:
                num_tables -+ 1

            avg_sq_diff = np.nan
            for col in col_names:
                if col != 'zip':
                    table = col.split('_')[0]
                    num_vars = table_counts[table]
                    if col.startswith('weather'):
                        num_vars = num_weather_vars
                    num_bins = 1
                    if table == 'census':
                        for var in census_dist_counts:
                            if re.search(var, col):
                                num_bins = census_dist_counts[var]
                    wgt = (num_vars * num_bins * num_tables)
                    sq_diff = (row[col] - start_zip_data[col].values[0]) ** 2
                    avg_sq_diff = np.nansum([avg_sq_diff, sq_diff * (1 / wgt)])
                    if avg_sq_diff >= best_avg_sq_diff5:
                        break
            if avg_sq_diff >= best_avg_sq_diff5: # make this better, maybe put one of these loops into a func
                continue
            if not np.isnan(avg_sq_diff):
                if avg_sq_diff >= best_avg_sq_diff4:
                    index = 4
                elif avg_sq_diff >= best_avg_sq_diff3:
                    index = 3
                elif avg_sq_diff >= best_avg_sq_diff2:
                    index = 2
                elif avg_sq_diff >= best_avg_sq_diff1:
                    index = 1
                else:
                    index = 0
                self.best_zips.pop()
                self.best_zips.insert(index, (row['zip'], avg_sq_diff))
        self.compute_scores()


    def compute_scores(self):
        '''
        INSERT HEADER
        '''
        best_zip5, best_avg_sq_diff5 = self.best_zips[4]
        best_zip4, best_avg_sq_diff4 = self.best_zips[3]
        best_zip3, best_avg_sq_diff3 = self.best_zips[2]
        best_zip2, best_avg_sq_diff2 = self.best_zips[1]
        best_zip1, best_avg_sq_diff1 = self.best_zips[0]

        best_score5 = 100 * (1 - stats.chi2.cdf(best_avg_sq_diff5, 1))
        best_score4 = 100 * (1 - stats.chi2.cdf(best_avg_sq_diff4, 1))
        best_score3 = 100 * (1 - stats.chi2.cdf(best_avg_sq_diff3, 1))
        best_score2 = 100 * (1 - stats.chi2.cdf(best_avg_sq_diff2, 1))
        best_score1 = 100 * (1 - stats.chi2.cdf(best_avg_sq_diff1, 1))

        self.best_zips = [(best_zip1, best_score1),
                          (best_zip2, best_score2),
                          (best_zip3, best_score3),
                          (best_zip4, best_score4),
                          (best_zip5, best_score5)]


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
    state = args_from_ui['input_state']
    start_zip = args_from_ui['input_zip'] # don't do this twice?
    tables = args_from_ui['tables']

    var_name_lst = []
    join_statement = ''
    for table in tables:
        var_name_lst.append(''.join([table, '.*']))
        join_statement = ' '.join([join_statement, 'JOIN', table, 'USING (zip)'])
    var_names = ', '.join(var_name_lst)
    preamble = ' '.join(['SELECT', var_names, 'FROM census AS c'])
    conditions = 'WHERE c.state = ? OR c.zip = ?;'

    sql_query = ' '.join([preamble, join_statement, conditions])
    args = (state, start_zip)

    return (sql_query, args)


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

    zip_info.compute_sq_diffs()
    return zip_info.best_zips



# args_from_ui = {'input_state' : 'OH', 'input_zip' : 60637, 'tables' : ['census', 'business_count', 'great_schools', 'ideology', 'libraries', 'museums', 'walk_score', 'weather', 'zillow']}

# in orig algorithm, scale all variables to normalize, change denom of 88 to 23, add pop density
# use apply instead of loops, use itertuples for dfs and iteritems for series
# look at comments
# Chat with Shashank and Caroline about the scores

# pylint, git, close ssh
