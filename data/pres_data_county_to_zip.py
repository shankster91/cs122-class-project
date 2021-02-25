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
    pres_data = pres_data.drop(['county', 'state'], axis=1)
    pres_data.rename(columns = {'FIPS' : 'county', 'state_po' : 'state'}, inplace=True)
    pres_data['party'].fillna('other', inplace=True)
    pres_data = pres_data.merge(county_to_zip, how='left', on='county')
    cols_to_keep = ['state', 'zip', 'party', 'candidatevotes', 'totalvotes', 'res_ratio']
    pres_data = pres_data[cols_to_keep]
    vote_counts = ['candidatevotes', 'totalvotes']
    pres_data[vote_counts] = pres_data[vote_counts].multiply(pres_data['res_ratio'], axis=0)
    # fix ak data, count zips, see if accurate
    pres_data = pres_data.groupby(['state', 'zip', 'party'])[vote_counts].sum()
    # count 33,000
    # check total vote for accuracy          
    pres_data['vote_perc'] = (data['candidatevotes'] / data['totalvotes']) * 100
    # check that zips in ame county have same perc
    cols_to_drop = ['candidatevotes', 'totalvotes']
    pres_data = pres_data.drop(cols_to_drop, axis=1)
    pres_data =  pres_data.pivot_table(index=["state", "zip"],
                                       columns='party',
                                       values='vote_perc') # long to wide
    # drop absentee, no state_po, nan zip etc.
    data.to_csv('pres_data.csv', index=False)
    # count 33,000
    # examine data
    # break up into two functions, rename file
    # clean up code
