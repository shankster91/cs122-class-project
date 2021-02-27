'''
File that divides a zip-code-level count by land area to compute density.
'''

import pandas as pd


def compute_density(data):
    '''
    Compute density by dividing the zip-code-level counts by the zip code's land
    area in square miles.

    Inputs:
        data: A pandas dataframe.

    Outputs:
        A pandas dataframe that contains a measure of density for the
          supplied counts.
    '''
    columns = data.columns[data.columns != 'zip']
    data = data.astype('int64')
    land_area = pd.read_table('raw_data/zcta_land_area.txt')
    land_area.rename(columns = {'GEOID' : 'zip'}, inplace=True)
    density_data = data.merge(land_area, how='left', on='zip')
    return density_data[columns].divide(density_data['ALAND_SQMI'], axis=0)
