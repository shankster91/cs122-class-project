'''
File that pulls in zip-code-level Census data for the entire U.S.

To download the census module: pip install censusdata
To download the us module: pip install us
'''

import censusdata
import us
import compute_density

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
           'DP03_0027PE',
           'DP03_0028PE',
           'DP03_0029PE',
           'DP03_0030PE',
           'DP03_0031PE',
           'DP02_0058PE',
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
           'DP03_0119PE',
           'DP02_0153PE',
           'DP04_0046PE',
           'DP04_0047PE',
           'DP04_0003PE',
           'DP03_0097PE',
           'DP03_0098PE',
           'DP03_0099PE',
           'DP04_0141PE',
           'DP04_0142PE',
           'DP03_0002PE',
           'DP03_0005PE',
           'DP02_0002PE',
           'DP02_0004PE',
           'DP02_0007PE',
           'DP02_0008PE',
           'DP02_0011PE',
           'DP02_0012PE',
           'DP02_0014PE',
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
             'income_under_10,000',
             'income_10,000-14,999',
             'income_15,000-24,999',
             'income_25,000-34,999',
             'income_35,000-49,999',
             'income_50,000-74,999',
             'income_75,000-99,999',
             'income_100,000-149,999',
             'income_150,000-199,999',
             'income_over_200,000',
             'educ_less_than_9th_grade',
             'educ_some_high_school',
             'educ_high_school_diploma',
             'educ_some_college',
             'educ_associates_degree',
             'educ_bachelors_degree',
             'educ_graduate_degree',
             'management_biz_science_arts_occupations',
             'service_occupations',
             'sales_office_occupations',
             'resources_construction_maintenance_occupations',
             'production_transport_moving_occupations',
             'student',
             'male',
             'female',
             'race_white',
             'race_black',
             'race_native_american',
             'race_asian',
             'race_pacific_islander',
             'other_race',
             'ethnicity_arab',
             'ethnicity_hispanic',
             'native_born',
             'foreign_born',
             'english_language',
             'spanish_language',
             'males_never_married',
             'males_married',
             'males_separated',
             'males_widowed',
             'males_divorced',
             'females_never_married',
             'females_married',
             'females_separated',
             'females_widowed',
             'females_divorced',
             'below_poverty_level',
             'HHs_w_internet',
             'owner-occupied_housing',
             'renter-occupied_housing',
             'vacant_housing',
             'private_health_insurance',
             'public_health_insurance',
             'no_health_insurance',
             'housing_insecure1',
             'housing_insecure2',
             'lfpr',
             'unemployment_rate',
             'struct_married_couple',
             'struct_cohabitating_couple',
             'struct_male_HHer_w_children',
             'struct_male_HHer_wo_children',
             'struct_female_HHer_w_children',
             'struct_female_HHer_wo_children',
             'HHs_w_children',
             'HHer_moved_after_2017',
             'HHer_moved_2015-2016',
             'HHer_moved_2010-2014',
             'HHer_moved_2000-2009',
             'HHer_moved_1990-1999',
             'HHer_moved_before_1989']


def pull_census_data():
    '''
    Pulls basic demographic data at the zip code level from the 5-year American
    Community Survey. Writes the data to a csv called census_data.csv.

    Inputs:
        None

    Outputs:
        None
    '''
    data = censusdata.download('acs5', 2019,
                               censusdata.censusgeo([('state', '*'),
                                            ('zip code tabulation area', '*')]),
                               var_lst, tabletype='profile')
    data.columns = col_names
    zip_codes = []
    state_abbrs = []
    for label in data.index:
        state_code = label.geo[0][1]
        state = us.states.lookup(state_code) # convert the FIPS codes to state postal codes
        state_abbrs.append(state.abbr)
        zip_code = label.geo[1][1]
        zip_codes.append(zip_code)
    data.insert(0, 'state', state_abbrs)
    data.insert(1, 'zip', zip_codes)
    data.reset_index(drop=True, inplace=True)
    data['pop_density'] = compute_density.compute_density(data[['zip', 'total_pop']])
    data.drop('total_pop', axis=1, inplace=True)
    data.to_csv('census_data.csv', index=False)
