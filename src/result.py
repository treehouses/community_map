import json

from src.communicate_db import get_db
from src.communicate_db import count_rows
from env import LOCAL_DB_URL
from env import headers_local

def erase_duplicate(finallist):

    text = "LAT,LONG,times\n"
    duplicates = []
    for item in finallist:
        if finallist.count(item) > 0:
            duplicates.append(finallist.count(item))
    for i in range(len(finallist)):
        finallist[i] = finallist[i] + "," + str(duplicates[i])
    finallist = list(set(finallist))
    for i in range(len(finallist)):
        text += finallist[i] + "\n"
    return text

def produce_new_csv():
    
    local_db_data = get_db(
        LOCAL_DB_URL,
        headers=headers_local,
        params={"limit": count_rows(LOCAL_DB_URL, headers=headers_local)})
    finallist = [ 
        f"{data['approx_latitude']},{data['approx_longitude']}"
        for data in json.loads(local_db_data)['results']
    ]

    text = erase_duplicate(finallist)
    filename = "./data/treehouses.csv"
    with open(filename, "w") as outp:
            outp.write(text)
    
    print("Produce the new csv file")