'''
This file creates the final dataset for 2016 presidential election results by
converting the data from county level to zip code level.

For each zip code, the county-level vote counts for the county(ies) containing
the zip code are multiplied by the fraction of the county's population that
resides in that zip code. When a zip code straddles multiple counties, we
take the sum of the population-weighted vote counts across the counties that the
zip code straddles.

To download the xlrd module: pip install xlrd
To download the openpyxl module: pip install openpyxl
'''

import pandas as pd

def county_to_zip():
    '''
    Converts the presidential election results data from county level to
    zip code level, and writes the data to a csv called pres_data.csv.

    Inputs:
        None
    
    Outputs:
        None
    '''
    pres_data = pd.read_csv('raw_data/2016_US_County_Level_Presidential_Results.csv')
    county_to_zip = pd.read_excel('raw_data/COUNTY_ZIP_122016.xlsx')
    county_to_zip.columns = [col.lower() for col in county_to_zip.columns]
    pres_data.rename(columns = {'combined_fips' : 'county', 'state_abbr' : 'state'}, inplace=True)
    pres_data['votes_other'] = pres_data['total_votes'] - pres_data['votes_dem'] - pres_data['votes_gop']
    pres_data = pres_data.merge(county_to_zip, how='left', on='county')
    cols_to_keep = ['state', 'zip', 'votes_dem', 'votes_gop', 'votes_other', 'total_votes', 'res_ratio']
    pres_data = pres_data[cols_to_keep]
    votes = ['votes_dem', 'votes_gop', 'votes_other', 'total_votes']
    pres_data.loc[:, votes] = pres_data[votes].multiply(pres_data['res_ratio'], axis=0)
    pres_data = pres_data.groupby(['state', 'zip'])[votes].sum().reset_index()
    party_votes = votes[:-1]
    pres_data.loc[:, party_votes] = pres_data[party_votes].divide(pres_data['total_votes'], axis=0) * 100
    pres_data.drop(['total_votes'], axis=1, inplace=True)
    pres_data.to_csv('pres_data.csv', index=False)

    # break up into two functions, rename file;  zip 39281, 7.7447 other
    # clean up code, pylint for pull census and clean pres
