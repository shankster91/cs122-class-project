'''
This file creates the final dataset for the count of business establishments
by type by zip code. It writes the final dataset to a csv called
business_count.csv located in the data folder

The original txt file is from Economic Census Report and it's joined with
the provided data dictionary to find the count of business establishment types
in every zip code in America
'''

import pandas as pd
import utils

biz_detail = pd.read_csv("data/raw_data/zbp18detail_sample.txt", encoding="cp1252",
                         dtype = {"zip": object, "naics": str})
biz_codes = pd.read_csv("data/raw_data/naics_codes_2017.txt", encoding="cp1252",
                        dtype = {"NAICS": str})
biz_codes.rename(columns = {"NAICS": "naics", "DESCRIPTION": "description"},
                 inplace = True)

biz = biz_detail.merge(biz_codes, on = "naics")

codes_select = list(biz_codes[biz_codes["naics"].str.contains("----")][1:]["naics"])
columns_select = ["zip", "est", "description"]

biz_detail_select = biz[biz["naics"].isin(codes_select)].loc[:, columns_select]

biz_count_pivot = biz_detail_select.pivot_table(index = "zip",
                                                columns = "description",
                                                values = "est")
zips = biz_count_pivot.index.values
biz_count_pivot.reindex(range(0, 29197))
biz_count_pivot["zip"] = zips

biz_count = biz_count_pivot.fillna(0)

new_names = {"Accommodation and Food Services": "business_accomod_food_srvcs",
             "Administrative and Support and Waste Management and Remediation Services": \
             "business_admin_support_and_waste_mngmt",
             "Agriculture, Forestry, Fishing and Hunting": \
             "business_agri_forestry_fishing_hunting",
             "Arts, Entertainment, and Recreation": "business_arts_entertain",
             "Construction": "business_construction",
             "Educational Services": "business_schooling_services",
             "Finance and Insurance": "business_finance_and_insurance",
             "Health Care and Social Assistance": "business_hlth_care_social",
             "Industries not classified": "business_unclassified",
             "Information": "business_information",
             "Management of Companies and Enterprises": "business_mngmt",
             "Manufacturing": "business_manufacturing",
             "Mining, Quarrying, and Oil and Gas Extraction": "business_oil",
             "Other Services (except Public Administration)": "business_other",
             "Professional, Scientific, and Technical Services": \
             "business_profess_sci_tech_services",
             "Real Estate and Rental and Leasing": "business_real_estate",
             "Retail Trade": "business_retail",
             "Transportation and Warehousing": "business_transport_warehouse",
             "Utilities": "business_utilities",
             "Wholesale Trade": "business_wholesale_trade"}
biz_count.rename(columns = new_names, inplace = True)

biz_count["zip"] = biz_count["zip"].astype(str)
biz_count.reset_index(drop=True, inplace=True)

biz_count = utils.compute_density(biz_count)
biz_count.fillna(0, inplace=True)

biz_count.to_csv("data/business_count.csv", index=False)
