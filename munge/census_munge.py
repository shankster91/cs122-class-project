'''
Pulls basic demographic data at the zip code level from the 5-year American
Community Survey. Cleans the data by creating state and zip code variables and
by computing population desnity. Writes the final dataset to a csv called
census_data.csv.

To download the census module: pip install censusdata
To download the us module: pip install us
'''

import censusdata
import us
from munge import utils


var_lst = ['DP05_0001E',
           'DP02_0016E',
           'DP05_0005PE',
           'DP05_0006PE',
           'DP05_0007PE',
           'DP05_0008PE',
           'DP05_0009PE',
           'DP05_0010PE',
           'DP05_0011PE',
           'DP05_0012PE',
           'DP05_0013PE',
           'DP05_0014PE',
           'DP05_0015PE',
           'DP05_0016PE',
           'DP05_0017PE',
           'DP03_0052PE',
           'DP03_0053PE',
           'DP03_0054PE',
           'DP03_0055PE',
           'DP03_0056PE',
           'DP03_0057PE',
           'DP03_0058PE',
           'DP03_0059PE',
           'DP03_0060PE',
           'DP03_0061PE',
           'DP02_0060PE',
           'DP02_0061PE',
           'DP02_0062PE',
           'DP02_0063PE',
           'DP02_0064PE',
           'DP02_0065PE',
           'DP02_0066PE',
           'DP05_0002PE',
           'DP05_0003PE',
           'DP05_0037PE',
           'DP05_0038PE',
           'DP05_0039PE',
           'DP05_0044PE',
           'DP05_0052PE',
           'DP05_0057PE',
           'DP02_0125PE',
           'DP05_0071PE',
           'DP02_0088PE',
           'DP02_0093PE',
           'DP02_0112PE',
           'DP02_0115PE',
           'DP02_0026PE',
           'DP02_0027PE',
           'DP02_0028PE',
           'DP02_0029PE',
           'DP02_0030PE',
           'DP02_0032PE',
           'DP02_0033PE',
           'DP02_0034PE',
           'DP02_0035PE',
           'DP02_0036PE',
           'DP04_0046PE',
           'DP04_0047PE',
           'DP04_0003PE',
           'DP03_0002PE',
           'DP03_0005PE',
           'DP04_0051PE',
           'DP04_0052PE',
           'DP04_0053PE',
           'DP04_0054PE',
           'DP04_0055PE',
           'DP04_0056PE']

col_names = ['total_pop',
             'mean_HH_size',
             'under_age_5',
             'age_5-9',
             'age_10-14',
             'age_15-19',
             'age_20-24',
             'age_25-34',
             'age_35-44',
             'age_45-54',
             'age_55-59',
             'age_60-64',
             'age_65-74',
             'age_75-84',
             'over_age_85',
             'income_under_10000',
             'income_10000-14999',
             'income_15000-24999',
             'income_25000-34999',
             'income_35000-49999',
             'income_50000-74999',
             'income_75000-99999',
             'income_100000-149999',
             'income_150000-199999',
             'income_over_200000',
             'educ_less_than_9th_grade',
             'educ_some_high_school',
             'educ_high_school_diploma',
             'educ_some_college',
             'educ_associates_degree',
             'educ_bachelors_degree',
             'educ_graduate_degree',
             'sex_male',
             'sex_female',
             'race_white',
             'race_black',
             'race_native_american',
             'race_asian',
             'race_pacific_islander',
             'other_race',
             'race_arab',
             'race_hispanic',
             'native_birth_place',
             'foreign_birth_place',
             'english_language',
             'spanish_language',
             'marital_males_never_married',
             'marital_males_married',
             'marital_males_separated',
             'marital_males_widowed',
             'marital_males_divorced',
             'marital_females_never_married',
             'marital_females_married',
             'marital_females_separated',
             'marital_females_widowed',
             'marital_females_divorced',
             'owner-occupied_housing',
             'renter-occupied_housing',
             'unoccupied_housing',
             'lfpr',
             'unemployment_rate',
             'last_move_after_2017',
             'last_move_2015-2016',
             'last_move_2010-2014',
             'last_move_2000-2009',
             'last_move_1990-1999',
             'last_move_before_1989']

data = censusdata.download('acs5', 2019,
                           censusdata.censusgeo([('state', '*'),
                                            ('zip code tabulation area', '*')]),
                           var_lst, tabletype='profile')
data.columns = col_names
data = data.add_prefix('census_')

data = data[data >= 0].dropna(how='any')

zip_codes = []
state_abbrs = []
for label in data.index:
    state_code = label.geo[0][1]
    state = us.states.lookup(state_code) # convert FIPS to state postal codes
    state_abbrs.append(state.abbr)
    zip_code = int(label.geo[1][1])
    zip_codes.append(zip_code)
data.insert(0, 'state', state_abbrs)
data.insert(1, 'zip', zip_codes)
data.reset_index(drop=True, inplace=True)

pop_density_data = utils.compute_density(data[['zip', 'census_total_pop']])
pop_density_data.columns = ['zip', 'census_pop_density']
data = data.merge(pop_density_data, how='left', on='zip')
data.drop('census_total_pop', axis=1, inplace=True)

data.to_csv('data/census_data.csv', index=False)
