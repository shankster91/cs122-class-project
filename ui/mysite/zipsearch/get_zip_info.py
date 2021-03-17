'''
This file gets zip data from the zips returned by the matching algorithm
'''

import json
from pyzipcode import ZipCodeDatabase
from uszipcode import SearchEngine

def get_zip_info(res):
    '''
    Gets info on a zip code to be used for the map.

    Input:
    res (list of tuples): List of top zip code matches from the algorithm

    Output:
    zifo_list (list of lists): Info on each zip - city, state, latitude,
      longitude
    bounds_list (list of dictionaries): North, South, East, West lat/long bounds
      for each zip
    '''

    zcdb = ZipCodeDatabase()
    search = SearchEngine(simple_zipcode=True)
    zinfo_list = []
    bounds_list = []

    for i, tup in enumerate(res):
        bounds = {}
        _zip, _ = tup
        zip_info = search.by_zipcode(_zip)
        bounds['north'] = zip_info.bounds_north
        bounds['south'] = zip_info.bounds_south
        bounds['east'] = zip_info.bounds_east
        bounds['west'] = zip_info.bounds_west
        latitude = zip_info.lat
        longitude = zip_info.lng
        if zip_info.lat is None:
            try:
                zip_cln = int(_zip.lstrip("0"))
                zip_info = zcdb[zip_cln]
                latitude = zip_info.latitude
                longitude = zip_info.longitude
            except KeyError:
                pass
        zip_txt = "Match #" + str(i+1) + ": " + _zip + "<br>" \
                  + zip_info.city + ", " + zip_info.state
        zinfo_list.append([zip_txt, latitude, longitude])
        bounds_list.append(json.dumps(bounds))

    return zinfo_list, bounds_list
