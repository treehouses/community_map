
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

def _make_mac_and_location_df(data):

    data = data.groupby(['approx_latitude', 'approx_longitude', 'bluetoothMacAddress'],
                        as_index=False).size().astype({'bluetoothMacAddress': 'string'})
    # .round({'approx_latitude':3, 'approx_longitude':3})
    data = data[data['bluetoothMacAddress'].str.match(
        r'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}')]
    
    lat = data['approx_latitude'].to_list()
    lng = data['approx_longitude'].to_list()
    mac_address = data['bluetoothMacAddress'].to_list()

    data_list = [[(lat[i], lng[i]), mac_address[i]] for i in range(len(lat))]

    latlng_mac_dict = {}
    for datum in data_list:

        key = datum[0]
        if not key in latlng_mac_dict.keys():
            latlng_mac_dict[key] = []
        latlng_mac_dict[key].append(datum[1].strip())
    
    prev_df = {
        'approx_latitude': [],
        'approx_longitude': [],
        'rpiNumber': []
    }
    for key, val in latlng_mac_dict.items():
        prev_df['approx_latitude'].append(key[0])
        prev_df['approx_longitude'].append(key[1])
        prev_df['rpiNumber'].append(str(len(val)))
    
    return pd.DataFrame(prev_df)

def analyze_mac_and_location(date=None):

    data = DATA.copy()
    data["originalUpdateTime"] = pd.to_datetime(data["originalUpdateTime"])
    data = data.set_index(data["originalUpdateTime"])

    if date:
        return _make_mac_and_location_df(data.loc[date])
    else:
        return _make_mac_and_location_df(data)

"""
    #data = data.groupby(['approx_latitude', 'approx_longitude'],
    #                    as_index=False).size().sort_values(by='approx_latitude')

    data.to_csv('./data/mac_and_location.csv', index=False)
    return data
"""

def get_device_manufacture():

    data = DATA.copy()
    for col_name in COL_NAME_LIST:
        DATA.copy().groupby(
            ['approx_latitude', 'approx_longitude',  col_name]).size().to_csv(f'data/geo_{col_name}.csv')
        DATA.copy().groupby([col_name, 'approx_latitude',
                            'approx_longitude']).size().to_csv(f'data/{col_name}_geo.csv')
