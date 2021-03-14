'''
This file contains utility functions used for data cleaning.
'''

import us
import pandas as pd


def compute_density(data):
    '''
    Compute density by dividing zip-code-level counts by zip code land area.

    Inputs:
        data: a pandas dataframe containing counts.

    Outputs:
        A pandas dataframe that contains measures of density for the
          supplied counts.
    '''
    columns = data.columns
    counts = columns[columns != 'zip']
    data = data.astype('int64')
    land_area = pd.read_table('data/raw_data/zcta_land_area.txt')
    land_area.rename(columns = {'GEOID' : 'zip'}, inplace=True)
    density_data = land_area.merge(data, how='left', on='zip')
    density_data[counts] = density_data[counts].divide(density_data['ALAND_SQMI'],
                                                       axis=0)
    return density_data[columns]


def county_to_zip(data):
    '''
    Map county-level data to zip codes.

    Inputs:
        data: a pandas dataframe containing county-level data.

    Outputs:
        A pandas dataframe containing county-level data for each zip code.
    '''
    county_zip_map = pd.read_excel('data/raw_data/COUNTY_ZIP_122016.xlsx')
    county_zip_map.columns = [col.lower() for col in county_zip_map.columns]
    data = data.merge(county_zip_map, how='left', on='county')
    return data


def extract_state_and_zip(index_name):
    '''
    Extracts a state abbreviation and a zip code from an index name.

    Inputs:
        index_name: a census geo object

    Outputs:
        A pandas series containing an integer representing a zip code and a
          string representing a state abbreviation.
    '''
    zip_code = int(index_name.geo[1][1])
    fips_code = index_name.geo[0][1]
    state = us.states.lookup(fips_code)
    return pd.Series([zip_code, state.abbr])
