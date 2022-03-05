import io
import json

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
        orient="records", dtype={'approx_latitude':'string', 'approx_longitude':'string'})
    return data

def analyze(date):

    data = get_data()
    data["originalUpdateTime"] = pd.to_datetime(data["originalUpdateTime"])
    data = data.set_index(data["originalUpdateTime"])
    data = data.loc[date].groupby(['approx_latitude', 'approx_longitude'], as_index=False).size()
    print(data)


def analyze_mac_and_location():

    data = get_data()
    data = data.groupby(['approx_latitude', 'approx_longitude', 'bluetoothMacAddress'], as_index=False).size().astype({'bluetoothMacAddress': 'string'})
    data = data[data['bluetoothMacAddress'].str.match(r'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}')]#.round({'approx_latitude':3, 'approx_longitude':3})

    data = data.groupby(['approx_latitude', 'approx_longitude'], as_index=False).size().sort_values(by='approx_latitude')
    data.to_csv('./data/mac_and_location.csv', index=False)
    return data
