import os

ROOT = os.getcwd()
GEO_API_URL = "http://geodb-free-service.wirefreethought.com/v1/geo/locations/"
LOCAL_DB_URL = 'You local DB URL here'
REMOTE_DB_URL = 'Treehouses DB URL here; ask Dogi'

headers = {"X-Parse-Application-Id": "Password is here",
            "X-Parse-REST-API-Key": "undefined"}

headers_local  = {"X-Parse-Application-Id": "Password is here",
            "X-Parse-REST-API-Key": "undefined"}

GEO_API_PARAMS = {"radius": 100, "minPopulation":40000, "limit": 1}
