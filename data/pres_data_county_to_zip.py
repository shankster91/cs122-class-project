'''
This file creates the final dataset for 2016 presidential election results by
converting the data from county level to zip code level.
'''

import pandas as pd

def county_to_zip():
    '''
    Converts the presidential election results data from county level to zip
    code level. For a given zip code, the county-level results for the county containing that zip code are multiplied by the fraction of the county's population that lives in that zip code. When a zipcode straddles multiple counties, the same process is followed but the population-weighted results for each county are summed across the counties in which the zip code lies.

    Inputs:
        None
    
    Output:
        
    '''
    eviction_data = pd.read_csv('eviction_data_tract.csv')
    tract_to_zip = pd.read_csv('tract_zip.csv')
    eviction_data = eviction_data.loc[eviction_data['filing_year']==2019]
    eviction_data = eviction_data.merge(tract_to_zip, how='left', on='tract')
    cols_to_keep = ['zip', 'eviction_filings_total', 'RES_RATIO']
    eviction_data = eviction_data[cols_to_keep]
    eviction_data = eviction_data.groupby('zip').apply(lambda row:
                          sum(row['eviction_filings_total'] * row['RES_RATIO']))
    eviction_data.name = 'eviction_filings'
    eviction_data.index = eviction_data.index.astype(str)
                          
    data = data.merge(eviction_data, how='left', left_index=True, right_index=True)
    data['eviction_filings_rate'] = (data['eviction_filings'] / data['rental_units']) * 100
    cols_to_drop = ['eviction_filings', 'rental_units']
    data = data.drop(cols_to_drop, axis=1)
    return data


