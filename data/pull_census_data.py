'''
File that pulls in zip-code-level Census data for the entire U.S.

To download the census module: pip install censusdata
To download the us module: pip install us
'''

import censusdata
import us
import re
import pandas as pd

var_lst = ['DP02_0016E', # mean household size
           'DP05_0005PE', # percentage of ppl under age 5
           'DP05_0006PE', # percentage of ppl age 5-9
           'DP05_0007PE', # percentage of ppl age 10-14
           'DP05_0008PE', # percentage of ppl age 15-19
           'DP05_0009PE', # percentage of ppl age 20-24
           'DP05_0010PE', # percentage of ppl age 25-34
           'DP05_0011PE', # percentage of ppl age 35-44
           'DP05_0012PE', # percentage of ppl age 45-54
           'DP05_0013PE', # percentage of ppl age 55-59
           'DP05_0014PE', # percentage of ppl age 60-64
           'DP05_0015PE', # percentage of ppl age 65-74
           'DP05_0016PE', # percentage of ppl age 75-84
           'DP05_0017PE', # percentage of ppl over age 85
           'DP03_0052PE', # percentage of HHs with annual income + benefits under $10,000
           'DP03_0053PE', # percentage of HHs with annual income + benefits $10,000-$14,999
           'DP03_0054PE', # percentage of HHs with annual income + benefits $15,000-$24,999
           'DP03_0055PE', # percentage of HHs with annual income + benefits $25,000-$34,999
           'DP03_0056PE', # percentage of HHs with annual income + benefits $35,000-$49,999
           'DP03_0057PE', # percentage of HHs with annual income + benefits $50,000-$74,999
           'DP03_0058PE', # percentage of HHs with annual income + benefits $75,000-$99,999
           'DP03_0059PE', # percentage of HHs with annual income + benefits $100,000-$149,999
           'DP03_0060PE', # percentage of HHs with annual income + benefits $150,000-$199,999
           'DP03_0061PE', # percentage of HHs with annual income + benefits over $200,000
           'DP02_0060PE', # percentage of ppl over 25 with less than 9th grade education
           'DP02_0061PE', # percentage of ppl over 25 with some high school
           'DP02_0062PE', # percentage of ppl over 25 with high school diploma
           'DP02_0063PE', # percentage of ppl over 25 with some college
           'DP02_0064PE', # percentage of ppl over 25 with associate's degree
           'DP02_0065PE', # percentage of ppl over 25 with bachelor's degree
           'DP02_0066PE', # percentage of ppl over 25 with graduate degree
           'DP03_0027PE', # percentage of ppl over 16 working in management, business, science, and arts occupations
           'DP03_0028PE', # percentage of ppl over 16 working in service occupations
           'DP03_0029PE', # percentage of ppl over 16 working in sales and office occupations
           'DP03_0030PE', # percentage of ppl over 16 working in natural resources, construction, and maintenance occupations
           'DP03_0031PE', # percentage of ppl over 16 working in production, transportation, and material moving occupations
           'DP02_0058PE', # percentage of ppl over 3 enrolled in college or graduate school
           'DP05_0002PE', # percentage of ppl who are male
           'DP05_0003PE', # percentage of ppl who are female
           'DP05_0037PE', # percentage of ppl who are white
           'DP05_0038PE', # percentage of ppl who are Black
           'DP05_0039PE', # percentage of ppl who are Native American
           'DP05_0044PE', # percentage of ppl who are Asian
           'DP05_0052PE', # percentage of ppl who are Native Hawaiian or Pacific Islander
           'DP05_0057PE', # percentage of ppl who are of some other race
           'DP02_0125PE', # percentage of ppl who are of Arab ancestry
           'DP05_0071PE', # percentage of ppl who are of Hispanic ancestry
           'DP02_0088PE', # percentage of ppl who are native born
           'DP02_0093PE', # percentage of ppl who are foreign born
           'DP02_0112PE', # percentage of ppl who speak English at home
           'DP02_0115PE', # percentage of ppl who speak Spanish at home
           'DP02_0026PE', # percentage of males over 15 who have never been married
           'DP02_0027PE', # percentage of males over 15 who are married
           'DP02_0028PE', # percentage of males over 15 who are separated
           'DP02_0029PE', # percentage of males over 15 who are widowed
           'DP02_0030PE', # percentage of males over 15 who are divorced
           'DP02_0032PE', # percentage of females over 15 who have never been married
           'DP02_0033PE', # percentage of females over 15 who are married
           'DP02_0034PE', # percentage of females over 15 who are separated
           'DP02_0035PE', # percentage of females over 15 who are widowed
           'DP02_0036PE', # percentage of females over 15 who are divorced
           'DP03_0119PE', # percentage of HHs below poverty level
           'DP02_0153PE', # percentage of HHs with an Internet subscription
           'DP04_0046PE', # percentage of housing units that are owner-occupied
           'DP04_0047PE', # percentage of housing units that are renter-occupied
           'DP04_0003PE', # percentage of housing units that are vacant
           'DP03_0097PE', # percentage of ppl with private health insurance
           'DP03_0098PE', # percentage of ppl with public health insurance
           'DP03_0099PE', # percentage of ppl with no health insurance
           'DP04_0141PE', # percentage of HHs putting 30-34.9% of their income toward rent
           'DP04_0142PE', # percentage of HHs putting more than 35% of their income toward rent
           'DP03_0002PE', # percentage of ppl over 16 who are in the labor force
           'DP03_0005PE', # percentage of ppl over 16 who are unemployed
           'DP02_0002PE', # percentage of HHs with a married couple
           'DP02_0004PE', # percentage of HHS with a cohabitating couple
           'DP02_0007PE', # percentage of HHs consisting of a male householder with children
           'DP02_0008PE', # percentage of HHs consisting of a male householder without children
           'DP02_0011PE', # percentage of HHs consisting of a female householder with children
           'DP02_0012PE', # percentage of HHs consisting of a female householder without children
           'DP02_0014PE', # percentage of HHs with children
           'DP04_0051PE', # percentage of HHers who have moved since 2017
           'DP04_0052PE', # percentage of HHers who last moved bw 2015-2016
           'DP04_0053PE', # percentage of HHers who last moved bw 2010-2014
           'DP04_0054PE', # percentage of HHers who last moved bw 2000-2009
           'DP04_0055PE', # percentage of HHers who last moved bw 1990-1999
           'DP04_0056PE'] # percentage of HHers who last moved before 1989

col_names = ['mean_HH_size',
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
    data.to_csv('census_data.csv', index=False)
