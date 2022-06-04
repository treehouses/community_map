import json
import io

import pandas as pd

from src.communicate_db import get_db, count_rows
from env import LOCAL_DB_URL
from env import headers_local

def get_data():

    local_db_data = get_db(
        LOCAL_DB_URL,
        headers=headers_local,
        params={"limit": count_rows(LOCAL_DB_URL, headers=headers_local)})
    data = pd.read_json(io.StringIO(
        json.dumps(json.loads(local_db_data)["results"])),
        orient="records", dtype={'approx_latitude': 'string', 'approx_longitude': 'string'})
    return data

DATA = get_data()