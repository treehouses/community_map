from src.communicate_db import get_db, count_rows
from env import LOCAL_DB_URL
from env import headers_local
import json
import io
import sys
import os

import pandas as pd

COL_NAME_LIST = ['deviceManufacturer', 'deviceName']


def get_data():

    local_db_data = get_db(
        LOCAL_DB_URL,
        headers=headers_local,
        params={"limit": count_rows(LOCAL_DB_URL, headers=headers_local)})
    data = pd.read_json(io.StringIO(
        json.dumps(json.loads(local_db_data)["results"])),
        orient="records", dtype={'approx_latitude': 'string', 'approx_longitude': 'string'})
    return data


def analyze(date):

    data = get_data()
    data["originalUpdateTime"] = pd.to_datetime(data["originalUpdateTime"])
    data = data.set_index(data["originalUpdateTime"])
    data = data.loc[date].groupby(
        ['approx_latitude', 'approx_longitude'], as_index=False).size()
    print(data)


def analyze_mac_and_location():

    data = get_data()
    data = data.groupby(['approx_latitude', 'approx_longitude', 'bluetoothMacAddress'],
                        as_index=False).size().astype({'bluetoothMacAddress': 'string'})
    # .round({'approx_latitude':3, 'approx_longitude':3})
    data = data[data['bluetoothMacAddress'].str.match(
        r'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}')]

    data = data.groupby(['approx_latitude', 'approx_longitude'],
                        as_index=False).size().sort_values(by='approx_latitude')
    data.to_csv('./data/mac_and_location.csv', index=False)
    return data


def get_device_manufacture():

    data = get_data()
    for col_name in COL_NAME_LIST:
        data.copy().groupby(
            ['approx_latitude', 'approx_longitude',  col_name]).size().to_csv(f'data/geo_{col_name}.csv')
        data.copy().groupby([col_name, 'approx_latitude',
                            'approx_longitude']).size().to_csv(f'data/{col_name}_geo.csv')
