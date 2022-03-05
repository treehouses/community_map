import json

from src.communicate_db import get_db
from src.communicate_db import count_rows
from env import REMOTE_DB_URL
from env import headers

def is_right_data(tempdata):

    # If the item has not gps_latitude value,
    # the item is useless
    if not tempdata['gps_latitude']:
        return False
    return True

def change_key(key):

    # DB does not take objectId and createdAt as keys
    # to make a new item
    if key == "objectId":
        return "originalObjId"
    if key == "createdAt":
        return "originalUpdateTime"
    return key 

def transform_data(tempdata_set: dict) -> dict:

    # Reuse almost all schema except several keys
    # data to upload the new item
    # on the another DB
    return [{
        change_key(key): val
        for key, val in tempdata.items() 
        if not key in ['versionCode', 'ACL', 'updatedAt', 'type', 'description']
    }  for tempdata in tempdata_set if is_right_data(tempdata)]

def get_new_data():

    params = {"limit": count_rows(REMOTE_DB_URL, headers=headers)}
    db_data = get_db(REMOTE_DB_URL, headers=headers ,params=params)
    if db_data:
        with open('./data/treehouses-log.json', 'w') as f:
            f.write(db_data)
        return json.loads(db_data).get("results", None)

def get_remote_db_dataset():

    temp = get_new_data()
    if temp:
        return transform_data(temp)
    print("remote db schema might be changed")
    return None