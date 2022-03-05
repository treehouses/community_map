import os
import re

from src.communicate_db import get_db
from env import GEO_API_URL
from env import GEO_API_PARAMS

def _add_plus_sign_if_not_minus(longitude):

    if longitude.find("-") == -1:
        longitude = f"+{longitude}"
    return longitude

def _get_gio_api_url(GEO_API_URL, latitude, longitude):

    return os.path.join(
        GEO_API_URL,
        f"{latitude}{_add_plus_sign_if_not_minus(longitude)}",
        "nearbyCities"
    )

def get_approx_geodata(latitude, longitude):

    data = get_db(
        _get_gio_api_url(GEO_API_URL, latitude, longitude),
        params=GEO_API_PARAMS
    )
    if len(re.findall(r'"latitude":(.+?),', data)) < 1:
        return None
    else:
        latit = re.findall(r'"latitude":(.+?),', data)[0]
        longit = re.findall(r'"longitude":(.+?),', data)[0]
        return {"approx_latitude": latit, "approx_longitude": longit}