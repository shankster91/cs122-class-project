'''
This file creates the final dataset for 2016 presidential election results by
converting the data from county level to zip code level.

For each zip code, the county-level results for the county(ies) containing
the zip code are multiplied by the fraction of the county's population that
resides in that zip code. When a zip code straddels multiple counties, we
take the sum of the population-weighted results across the counties that the
zip code straddles.

To download the xlrd module: pip install xlrd
To download the openpyxl module: pip install openpyxl
'''

import pandas as pd

def county_to_zip():
    '''
    Converts the 2016 presidential election results data from county level to
    zip code level, and writes the data to a csv called pres_data.csv.

    Inputs:
        None
    
    Outputs:
        None
    '''
    pres_data = pd.read_csv('raw_data/countypres_2000-2016.csv')
    county_to_zip = pd.read_excel('raw_data/COUNTY_ZIP_122016.xlsx')
    county_to_zip.columns = [col.lower() for col in county_to_zip.columns]
    pres_data = pres_data.loc[pres_data['year']==2016]
    pres_data = pres_data.drop(['county'], axis=1)
    pres_data.rename(columns = {'FIPS' : 'county'}, inplace=True)

    pres_data = pres_data.merge(county_to_zip, how='left', on='county') # left?, county data type (leading zeros)
    cols_to_keep = ['state_po', 'zip', 'party', 'candidatevotes', 'RES_RATIO']
    pres_data = pres_data[cols_to_keep]
    pres_data = pres_data.groupby('zip').apply(lambda row:
                                  sum(row['candidatevotes'] * row['RES_RATIO']))             
    pres_data['vote_perc'] = (data['candidatevotes'] / data['totalvotes']) * 100
    cols_to_drop = ['candidatevotes', 'totalvotes']
    pres_data = pres_data.drop(cols_to_drop, axis=1)
    pres_data =  pres_data.pivot_table(index=["state_po", "zip"],
                                       columns='party',
                                       values='vote_perc') # long to wide
    # drop absentee, no state_po, etc.
    data.to_csv('pres_data.csv', index=False)
    # count 3,000
    # count 33,000
