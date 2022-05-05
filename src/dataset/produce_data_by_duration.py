from datetime import date

import src.dataset.produce_dataset as dataset

MIN_MONTH = 1
MAX_MONTH = 12
MIN_YEAR = 2020

this_year = int(date.today().isoformat().split('-')[0])
this_month = date.today().isoformat().split('-')[1]

def generate_year():

    year_list = sorted([f'{this_year - i}' for i in range(this_year - (MIN_YEAR - 1))])
    return year_list

def generate_month():

    year_list = generate_year()
    month_list = []
    for year in year_list:
        for month in range(MIN_MONTH, MAX_MONTH+1):
            month_list.append(f'{year}-{"0"+str(month) if month < 10 else month}')
            if month_list[-1] == f'{this_year}-{this_month}':
                break
    return month_list

def produce(choice: str=''):

    if choice == 'all':
        for year in generate_year():
            dataset.produce_new_dataset(year, year, 'year')
        for month in generate_month():
            dataset.produce_new_dataset(month, month, 'month')
    else:
        year = generate_year()[-1]
        month = generate_month()[-1]
        if '-'.join(date.today().isoformat().split('-')[1:]) == '01-01':
            year = generate_year()[-2]
            month = generate_month()[-2]
        elif date.today().isoformat().split('-')[-1] == '01':
            month = generate_month()[-2]
        dataset.produce_new_dataset(year, year, 'year')
        dataset.produce_new_dataset(month, month, 'month')

