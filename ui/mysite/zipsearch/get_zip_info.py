'''
This file gets zip data from the zips returned by the matching algorithm
'''

from pyzipcode import ZipCodeDatabase
from uszipcode import SearchEngine
import json

def get_zip_info(res):

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
        if zip_info.lat == None:
            try:
                zip_cln = int(_zip.lstrip("0"))
                zip_info = zcdb[zip_cln]
                latitude = zip_info.latitude
                longitude = zip_info.longitude
            except KeyError:
                pass
        zip_txt = "Match #:" + str(i+1) + " " + _zip + "<br>" \
                  + zip_info.city + ", " + zip_info.state
        zinfo_list.append([zip_txt, latitude, longitude])
        bounds_list.append(json.dumps(bounds))

    return zinfo_list, bounds_list