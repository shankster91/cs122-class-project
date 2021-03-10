'''
This file contains the algorithm that computes the average squared difference
between the attributes of a user-specified starting zip code and the attributes
of each zip code in a user-specified state. The algorithm then selects the five
zip codes in that state that are most similar to the user-specified zip code
(i.e. the five zip codes with the smallest average squared difference).
'''

import math
import sqlite3
import json
import pandas as pd
import numpy as np
from scipy import stats
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class zipInfo(object):
    '''
    Class for representing zip-code-level data and for keeping track of the zip
      codes that are most similar to the user-specified zip code.
    '''

    def __init__(self, args_from_ui):
        '''
        Construct a data structure to hold the zip-code-level data and to keep
        track of the most similar zip codes.

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

        self.table_counts = get_counts(os.path.join(BASE_DIR, 'algorithm', 'table_counts.txt'))
        if 'census' in self.tables:
            self.census_dist_counts = get_counts(os.path.join(BASE_DIR, 'algorithm', 'census_dist_counts.txt'))

    def find_best_zips(self, row):
        '''
        Compute the average squared difference for the given zip code, and
        update zipInfo in place with the best zip code matches (i.e. the zip
        codes that have the smallest average squared difference).

        Inputs:
            row: a row of a pandas dataframe containing data for a zip code in
              the target state.

        Outputs:
            None
        '''
        num_tables, num_weather_vars = self.adjust_counts_for_nan(row)
        avg_sq_diff = self.compute_avg_sq_diff(row, num_tables, num_weather_vars)
        if avg_sq_diff and (not np.isnan(avg_sq_diff)):
            self.update_best_zips(row['zip'], avg_sq_diff)

    def adjust_counts_for_nan(self, row):
        '''
        Adjust the number of tables and weather variables to disregard
        variables/tables that contain only NANs for the given zip code.
        We are interested in weather variables, because weather is the only
        table that can have NANs for some variables but not for others.

        Inputs:
            row: a row of a pandas dataframe containing data for a zip code in
              the target state.

        Outputs:
            A tuple (num_tables, num_weather_vars), where num_tables is an
              integer respresenting the number of tables that have non-NAN
              values for the given zip code, and num_weather_vars is an integer
              representing the number of variables from the weather table that
              have non-NAN values for the given zip code.
        '''
        num_tables = len(self.tables)
        num_weather_vars = self.table_counts['weather']
        cols_w_nan = ('school', 'zillow', 'walk_score', 'votes_dem')
        for col in self.col_names:
            if col.startswith(cols_w_nan):
                if np.isnan(row[col] - self.start_zip_data[col].values[0]):
                    num_tables -= 1
            elif col.startswith('weather'):
                if np.isnan(row[col] - self.start_zip_data[col].values[0]):
                    num_weather_vars -= 1
        if num_weather_vars == 0:
            num_tables -= 1
        return (num_tables, num_weather_vars)

    def compute_avg_sq_diff(self, row, num_tables, num_weather_vars):
        '''
        Compute the average squared difference for the given zip code.
        Returns None if the average squared difference exceeds the average
        squared differences for the top five best zip code matches.

        Inputs:
            row: a row of a pandas dataframe containing data for a zip code in
              the target state.
            num_tables: an integer representing the number of tables that have
              non-NAN values for the given zip code.
            num_weather_vars: an integer representing the number of variables in
              the weather table that have non-NAN values for the given zip code.

        Outputs:
            avg_sq_diff: a float representing the average squared difference.
        '''
        avg_sq_diff = np.nan
        _, best_avg_sq_diff5 = self.best_zips[4] # avg sq diff for 5th best zip
        for col in self.col_names:
            if col != 'zip':
                words = col.split('_')
                table = words[0]
                num_vars = self.table_counts[table]
                if col.startswith('weather'):
                    num_vars = num_weather_vars
                num_bins = 1
                if table == 'census':
                    var = words[1]
                    num_bins = self.census_dist_counts[var]
                wgt = num_vars * num_bins * num_tables
                sq_diff = (row[col] - self.start_zip_data[col].values[0]) ** 2
                if not np.isnan(sq_diff):
                    avg_sq_diff = np.nansum([avg_sq_diff, sq_diff * (1 / wgt)])
                if avg_sq_diff >= best_avg_sq_diff5:
                    return None
        return avg_sq_diff

    def update_best_zips(self, zip_code, avg_sq_diff):
        '''
        Based on the average squared difference for the current zip code, update
        the top five best zip codes accordingly. Updates zipInfo in place.
        If there's a tie, we prioritize the zip code that was processed first.

        Inputs:
            zip_code: an integer representing a zip code in the target state.
            avg_sq_diff: a float representing the average squared difference
              for the given zip code.

        Outputs:
            None
        '''
        _, best_avg_sq_diff4 = self.best_zips[3] # avg sq diff for 4th best zip
        _, best_avg_sq_diff3 = self.best_zips[2] # avg sq diff for 3rd best zip
        _, best_avg_sq_diff2 = self.best_zips[1] # avg sq diff for 2nd best zip
        _, best_avg_sq_diff1 = self.best_zips[0] # avg sq diff for 1st best zip
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
        self.best_zips.insert(index, (zip_code, avg_sq_diff))

    def compute_scores(self):
        '''
        Convert each of the five smallest average squared differences to a score
        between 0 and 100, where 100 indicates a zip code that is perfectly
        similar to the starting zip code and 0 indicates a zip code that is
        perfectly disimilar to the starting zip code. Updates zipInfo in place.

        Inputs:
            None

        Outputs:
            None
        '''
        for i, tpl in enumerate(self.best_zips):
            zip_code, avg_sq_diff = tpl
            zip_code = str(int(zip_code))
            if len(str(zip_code)) == 4:
                zip_code = "0" + zip_code
            score = 100 * (1 - stats.chi2.cdf(avg_sq_diff / 2, 1))
            self.best_zips[i] = (zip_code, str(round(score, 1)) + '%')


def pull_data(args_from_ui):
    '''
    Pull zip-code-level data for the starting zip code and for all zip codes in
    the user-specified state.

    Inputs:
        args_from_ui: a dictionary containing the user-specified inputs

    Outputs:
        A pandas dataframe.
    '''
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'zip_db.sqlite3'))
    sql_query, args = create_sql_query(args_from_ui)
    data = pd.read_sql(sql_query, conn, params=args)
    conn.close()

    data = data.loc[:, ~data.columns.duplicated()]
    data.drop('state', axis=1, errors='ignore', inplace=True)
    data = data.astype(dtype=float)
    data[data.lt(0)] = np.nan

    # Drop rows only containing NANs
    data = data[(data.drop('zip', axis=1).notnull()).any(axis=1)]

    zips = data['zip']
    data.drop('zip', axis=1, inplace=True)
    data = (data - data.mean())/data.std() # normalize
    # Cap the z-scores at 4 / -4
    data[data > 4] = 4
    data[data < -4] = -4

    return pd.concat([zips, data], axis=1)


def create_sql_query(args_from_ui):
    '''
    Create a SQL query given user-specified parameters.

    Inputs:
        args_from_ui: a dictionary containing the user-specified inputs

    Outputs:
        A tuple containing 1) a string representing a SQL query, and 2) a tuple
          containing the query's arguments.
    '''
    state = args_from_ui['input_state']
    start_zip = args_from_ui['input_zip']
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
    Takes in the name of a text file containing variable/bin counts and returns
    the contents of that file in dictionary format.

    Inputs:
        filename: a string representing the name of a text file.

    Outputs:
        A dictionary
    '''
    with open(filename) as f:
        counts = f.read()
    return json.loads(counts)


def return_best_zips(args_from_ui):
    '''
    Given user-specified inputs, pull the relevant data and return the top
    five best zip code matches.

    Inputs:
        args_from_ui: a dictionary containing the user-specified inputs.

    Outputs:
        best_zips: a list of five tuples containing 1) a string representing a
          zip code, and 2) the similarity score corresponding to that zip code.
    '''
    tables = args_from_ui['tables']
    if not tables:
        return 'Please check at least one of the checkboxes.'

    zip_info = zipInfo(args_from_ui)

    if zip_info.start_zip_data.empty:
        return 'Either the specified zip code is not a valid zip code, or ' \
               'there is no data available for the specified preference ' \
               'categories for the specified zip code. Please input a valid ' \
               'zip code or select additional preference categories.'
    if zip_info.data.empty:
        return 'The specified state is not a valid state. Please input a ' \
               'valid state postal abbreviation.'

    zip_info.data.apply(zip_info.find_best_zips, axis=1)
    zip_info.compute_scores()
    return zip_info.best_zips
