'''
Utility functions for url requests. Borrowed from PA3 to help with URL requests.
'''

import requests

def get_request(url):
    '''
    Open a connection to the specified URL and if successful
    read the data.

    Inputs:
        url: must be an absolute URL

    Outputs:
        request object or None

    Examples:
        get_request("http://www.cs.uchicago.edu")
    '''

    try:
        r = requests.get(url)
        if r.status_code == 404 or r.status_code == 403:
            r = None
    except Exception:
        # Fail on any kind of error
        r = None

    return r


def read_request(request):
    '''
    Return data from request object.  Returns result or "" if the read
    fails..
    '''

    try:
        return request.text.encode('iso-8859-1')
    except Exception:
        print("read failed: " + request.url)
        return ""
        