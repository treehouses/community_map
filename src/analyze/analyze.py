
import pandas as pd

from src.analyze.get_data import DATA


COL_NAME_LIST = ['deviceManufacturer', 'deviceName']

def analyze(date=None):

    data = DATA.copy()
    data["originalUpdateTime"] = pd.to_datetime(data["originalUpdateTime"])
    data = data.set_index(data["originalUpdateTime"])
    if date:
        data = data.loc[date].groupby(
            ['approx_latitude', 'approx_longitude'], as_index=False).size()
        return data
    else:
        data = data.groupby(
            ['approx_latitude', 'approx_longitude'], as_index=False).size()
        return data


def analyze_mac_and_location():

    data = DATA.copy()
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

    data = DATA.copy()
    for col_name in COL_NAME_LIST:
        DATA.copy().groupby(
            ['approx_latitude', 'approx_longitude',  col_name]).size().to_csv(f'data/geo_{col_name}.csv')
        DATA.copy().groupby([col_name, 'approx_latitude',
                            'approx_longitude']).size().to_csv(f'data/{col_name}_geo.csv')
