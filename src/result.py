from enum import Enum
import json

from src.communicate_db import get_db
from src.communicate_db import count_rows
from env import LOCAL_DB_URL
from env import headers_local

class CSV_Row(Enum):
    FIRST_DATA_ROW = 1
    EMPTY_ROW = -1

class Geo_Data_Col(Enum):
    LAT = 0
    LONG = 1
    FREQUENCY = 2

def chain(start, *funcs):
    res = start
    for func in funcs:
        res = func(res)
    return res

def get_apprx_latlng_list(data):

    return [ 
        f"{data['approx_latitude']},{data['approx_longitude']}"
        for data in json.loads(data)['results']
    ]

def groupby_latlng(datalist):

    csv_data = "LAT,LNG,FREQUENCY\n"
    duplicates = []
    for data in datalist:
        if datalist.count(data) > 0:
            duplicates.append(datalist.count(data))
    for i in range(len(datalist)):
        datalist[i] = datalist[i] + "," + str(duplicates[i])
    datalist = list(set(datalist))
    for i in range(len(datalist)):
        csv_data += datalist[i] + "\n"
    return csv_data 

def trancate(data):

    return [ datum.split(',') for datum 
            in data.split('\n')[CSV_Row.FIRST_DATA_ROW.value:CSV_Row.EMPTY_ROW.value] ]

def make_function(data):

    data_second_last_index= len(data) - 2
    geo_call_func_middle = "".join(
        [ f"{datum},\n" if index <= data_second_last_index else f"{datum}" 
        for index, datum in enumerate(data) ])
    text_func = f"geo_call([ \
            {geo_call_func_middle} \
        ])"
    return text_func

def write_data(data, filename):

    with open(filename, "w") as outp:
            outp.write(data)
    print(f"Produce the new {filename.split('/')[-1]}")

def produce_new_dataset():
    
    local_db_data = get_db(
        LOCAL_DB_URL,
        headers=headers_local,
        params={"limit": count_rows(LOCAL_DB_URL, headers=headers_local)})

    apprx_latlng_and_freq_csv = chain(local_db_data, get_apprx_latlng_list, groupby_latlng)
    text_func = chain(apprx_latlng_and_freq_csv, trancate, make_function)

    write_data(apprx_latlng_and_freq_csv, "./data/data.csv")
    write_data(text_func, "./data/treehouses.js")