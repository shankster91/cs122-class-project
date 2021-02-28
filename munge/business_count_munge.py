
'''
Read in txt files from Economic Census Report and join to find 
count of business establishment types in every zip code in America
'''

import pandas as pd

business_detail = pd.read_csv("data/raw_data/zbp18detail.txt", encoding="cp1252", dtype = {'zip': object, "naics": str})
business_codes = pd.read_csv("data/raw_data/naics_codes_2017.txt", encoding="cp1252", dtype = {"NAICS": str})
business_codes.rename(columns = {"NAICS": "naics", "DESCRIPTION": "description"}, inplace = True)

business = business_detail.merge(business_codes, on = "naics")

codes_select = list(business_codes[business_codes["naics"].str.contains("----")][1:]['naics'])
columns_select = ["zip", "est", "description"]

business_detail_select = business[business['naics'].isin(codes_select)].loc[:,columns_select]

# doesn't work
business_count = business_detail_select.pivot_table(index = [business_detail_select.index.values, "zip"], columns = 'description', values = "est").reset_index('zip')

# works?
business_count_pivot = business_detail_select.pivot_table(index = "zip", columns = 'description', values = "est")
zips = business_count_pivot.index.values
business_count_pivot.reindex(range(0,29197))
business_count_pivot['business_zip'] = zips

business_count = business_count_pivot.fillna(0)

business_count.rename(columns = {"Accommodation and Food Services": "business_accomodation_and_food_services",
                                'Administrative and Support and Waste Management and Remediation Services': "business_admin_support_and_waste_mngmt",
                                'Agriculture, Forestry, Fishing and Hunting': "business_agriculture_forestry_fishing_hunting",
                                'Arts, Entertainment, and Recreation': "business_arts_entertain_rec", 
                                'Construction': "business_construction",
                                'Educational Services': "business_education_services", 
                                'Finance and Insurance': "business_finance_and_insurance",
                                'Health Care and Social Assistance':"business_health_care_social_assit", 
                                'Industries not classified':"business_unclassified",
                                'Information': "business_information",
                                'Management of Companies and Enterprises': "business_mngmt_companies",
                                'Manufacturing': "business_manufacturing", 
                                'Mining, Quarrying, and Oil and Gas Extraction': "business_oil_extraction",
                                'Other Services (except Public Administration)': "business_other_services",
                                'Professional, Scientific, and Technical Services': "business_profess_scientif_tech_services",
                                'Real Estate and Rental and Leasing': "business_real_estate_rental_leasing", 
                                'Retail Trade':"business_retail",
                                'Transportation and Warehousing':"business_transportation_warehousing", 
                                'Utilities':"business_utilities", 
                                'Wholesale Trade':"business_wholesale_trade" 
                                }, inplace = True)

business_count['business_zip'] = business_count['business_zip'].astype(str)

business_count.to_csv("business_count.csv", index=False)

