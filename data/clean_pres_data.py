'''
This file creates the final dataset for 2016 presidential election results.

For each zip code, the county-level vote counts for the county(ies) containing
the zip code are multiplied by the fraction of the county's population that
resides in that zip code. When a zip code straddles multiple counties, we
take the sum of the population-weighted vote counts across the counties that the
zip code straddles.

To download the xlrd module: pip install xlrd
To download the openpyxl module: pip install openpyxl
'''

import pandas as pd

def county_to_zip(data):
    '''
    Converts data from county level to zip code level.

    Inputs:
        data: a pandas dataframe containing county-level data
    
    Outputs:
        A pandas dataframe containing the original data and the zip codes
          located in each county.
    '''
    county_to_zip = pd.read_excel('raw_data/COUNTY_ZIP_122016.xlsx')
    county_to_zip.columns = [col.lower() for col in county_to_zip.columns]
    return data.merge(county_to_zip, how='left', on='county')


def clean_pres_data():
    '''
    Clean the presidential election results data by renaming variables,
    calculating the vote counts for non-major parties, converting the data from
    county level to zip code level, and converting vote counts to percentages.
    Write the final dataset to a csv called pres_data.csv.

    Inputs:
        None
    
    Outputs:
        None
    '''
    pres_data = pd.read_csv('raw_data/2016_US_County_Level_Presidential_Results.csv')
    new_names = {'combined_fips' : 'county', 'state_abbr' : 'state'}
    pres_data.rename(columns = new_names, inplace=True)
    pres_data['votes_other'] = pres_data['total_votes'] \
                               - pres_data['votes_dem'] - pres_data['votes_gop']
    pres_data = county_to_zip(pres_data)
    votes = ['votes_dem', 'votes_gop', 'votes_other', 'total_votes']
    party_votes = votes[:-1]
    cols_to_keep = ['state', 'zip', 'res_ratio'] + votes
    pres_data = pres_data[cols_to_keep]
    # Multiply by the fraction of the county's population that resides in a zip
    pres_data.loc[:, votes] = pres_data[votes].multiply(pres_data['res_ratio'], 
                                                        axis=0)
    # Sum across the counties that a zip code straddles
    pres_data = pres_data.groupby(['state', 'zip'])[votes].sum().reset_index()
    pres_data.loc[:, party_votes] = pres_data[party_votes].divide(pres_data['total_votes'],
                                                                  axis=0) * 100
    pres_data.drop(['total_votes'], axis=1, inplace=True)
    pres_data.to_csv('pres_data.csv', index=False)

    # zip 39281, 7.7447 other
    # try division and multiplication
    # pylint for pull census and clean pres
