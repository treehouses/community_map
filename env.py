import os

if os.getcwd() == '/home/runner/work/communitymap/communitymap':

    GEO_API_URL = os.environ["GEO_API_URL"]
    LOCAL_DB_URL = os.environ["LOCAL_DB_URL"]
    REMOTE_DB_URL = os.environ["REMOTE_DB_URL"]
    HEADER_KEY  = os.environ["HEADER_KEY"]
    HEADER_LOCAL_KEY = os.environ["HEADER_LOCAL_KEY"]
else:
    import secrets 

    GEO_API_URL = secrets.GEO_API_URL
    LOCAL_DB_URL = secrets.LOCAL_DB_URL
    REMOTE_DB_URL = secrets.REMOTE_DB_URL
    HEADER_KEY  = secrets.HEADER_KEY
    HEADER_LOCAL_KEY = secrets.HEADER_LOCAL_KEY

ROOT = os.getcwd()
headers = {"X-Parse-Application-Id": HEADER_KEY,
            "X-Parse-REST-API-Key": "undefined"}

headers_local  = {"X-Parse-Application-Id": HEADER_LOCAL_KEY,
            "X-Parse-REST-API-Key": "undefined"}

GEO_API_PARAMS = {"radius": 100, "minPopulation":40000, "limit": 1}
