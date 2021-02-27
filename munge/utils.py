'''
File that contains functions for computing density and for converting data from
county level to zip code level.
'''

import pandas as pd


def compute_density(data):
    '''
    Compute density by dividing the zip-code-level counts by the zip code's land
    area in square miles.

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
    Convert data from county level to zip code level.

    Inputs:
        data: a pandas dataframe containing county-level data.

    Outputs:
        A pandas dataframe containing the county-level data for each zip code.
    '''
    county_zip_map = pd.read_excel('data/raw_data/COUNTY_ZIP_122016.xlsx')
    county_zip_map.columns = [col.lower() for col in county_zip_map.columns]
    data = data.merge(county_zip_map, how='left', on='county')
    return data
