import json
import requests

from env import LOCAL_DB_URL
from env import headers_local

class APICallingError(Exception):
    """Exception raised for errors in the API error.
    """

    def __init__(self, status_code):
        self.message = f"The status code is {status_code}"
        super().__init__(self.message)


def send_db(url: str, payloads: dict, headers={}) -> None:
    """Updates database by POST request
    
    Check out the below url for detail
    https://docs.parseplatform.org/rest/guide/#updating-objects

    Parameters
    ----------
    url
        Database of the URL
    payloads:
        Object to be added on the DB
    """

    headers["Content-Type"] = "application/json"
    r = requests.post(url, data=json.dumps(payloads), headers=headers)

    if not r.status_code == 201:
        raise APICallingError(r.status_code)


def get_db(url: str, headers={}, params={}) -> str:
    """Retrieve objects
    
    Check out the below url for detail
    https://docs.parseplatform.org/rest/guide/#retrieving-objects
    """
    
    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 200:
        return r.text
    else:
        raise  APICallingError(r.status_code)

def _convert_str_to_int(num: str) -> int:

    try:
        return(int(num))
    except ValueError:
        print("You cannot get number from remote db")
        exit()

def count_rows(path: str, headers={}) -> int:
    """Count number of object
    
    Check out the below url for the detail
    https://docs.parseplatform.org/rest/guide/#counting-objects
    """

    data = get_db(path, headers=headers, params={"count":1, "limit":0})
    if data:
        return _convert_str_to_int(json.loads(data)["count"])

def get_local_id_list():
    """Get local id list
    
    This local id list is used to check out whether the items
    from remote database is new or not
    """

    local_db_data = get_db(
        LOCAL_DB_URL,
        headers=headers_local,
        params={"limit": count_rows(LOCAL_DB_URL, headers=headers_local)})
    if local_db_data:
        return [data['originalObjId'] for data in json.loads(local_db_data)['results']]
