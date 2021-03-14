'''
This file creates the final dataset for the 2016 presidential election
results. It writes the final dataset to a csv called ideology_data.csv.

County-level data is converted to zip-code level. For each zip code, the
county-level vote counts for the county(ies) containing the zip code are
multiplied by the fraction of the county's population that resides in that zip
code. When a zip code straddles multiple counties, we take the sum of the
population-weighted vote counts across the counties that the zip code straddles.

Finally, the zip-code-level election results are converted into percentage terms.
'''

import pandas as pd
from munge import utils


data = pd.read_csv('data/raw_data/2016_US_County_Level_Presidential_Results.csv')
data.rename(columns = {'combined_fips' : 'county'}, inplace=True)
data['votes_other'] = data['total_votes'] - data['votes_dem'] - data['votes_gop']

data = utils.county_to_zip(data)

votes = ['votes_dem', 'votes_gop', 'votes_other', 'total_votes']
party_votes = votes[:-1]
cols_to_keep = ['zip', 'res_ratio'] + votes
data = data[cols_to_keep]

data.loc[:, votes] = data[votes].multiply(data['res_ratio'], axis=0)
data = data.groupby(['zip'])[votes].sum().reset_index()

data.loc[:, party_votes] = data[party_votes].divide(data['total_votes'],
                                                    axis=0) * 100

data.drop('total_votes', axis=1, inplace=True)
data.fillna(-1, inplace=True)

data.to_csv('data/ideology_data.csv', index=False)
