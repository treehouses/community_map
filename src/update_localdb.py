#!/usr/bin/env python3

# Converts exact coordinates from Google android studio collected data
# To city specific long/lat values so to avoid privacy concerns
# takes a file as input

import time

from src.communicate_db import send_db
from src.communicate_db import get_local_id_list
from src.download_remote_db import get_remote_db_dataset
from src.geodata import get_approx_geodata
from env import LOCAL_DB_URL
from env import headers_local

def store_newdata_local_db():

    id_list = get_local_id_list()
    dataset = get_remote_db_dataset()
    
    
    for data in dataset:
        if not data['originalObjId'] in id_list:
            approximaete_geo_dict = get_approx_geodata(data['gps_latitude'], data['gps_longitude'])
            if approximaete_geo_dict:
                data.update(approximaete_geo_dict)
                send_db(LOCAL_DB_URL, payloads=data, headers=headers_local)
                print(f"upload {data['originalObjId']}")
                time.sleep(1)
    print("All data is uploaded")
