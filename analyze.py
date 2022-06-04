import pandas as pd
import math

color_num = 12 
range_list = [[0,0] for _ in range(color_num)]

raw = pd.read_csv('data/year/2020.csv')
count_df = raw.copy()
count_df = count_df.groupby(['size']).count().iloc[:, 0].to_dict()

total = sum([ v for k, v in count_df.items()])
criterion_num = math.floor(total/color_num)


range_list_index = 0
min_max_index = 0

for k, v in count_df.items():

    if criterion_num > 0:
        if not min_max_index:
            range_list[range_list_index][min_max_index] = k
            total = total - v
            criterion_num = criterion_num - v
            min_max_index = 1
        else:
            total = total - v
            criterion_num = criterion_num - v
            range_list[range_list_index][min_max_index] = k
    else:
        range_list[range_list_index][min_max_index] = k
        min_max_index = 0
        range_list_index = range_list_index + 1
        range_list[range_list_index][min_max_index] = k
        total = total - v
        color_num = color_num - 1
        criterion_num = math.floor(total/color_num) 
        if not criterion_num: criterion_num = 1

for r in range_list:
    print(r)
    print()





