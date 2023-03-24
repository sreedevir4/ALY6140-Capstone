# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 22:31:31 2023

@author: sreed
"""

import requests
import csv
import pandas as pd



def api(url):
    response = requests.get(url)
    res = response.json()
    crime_data = res['result']['records']
    headers = list(crime_data[0].keys())
    with open('data.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames = headers)
        writer.writeheader() 
        for row in crime_data:
            writer.writerow(row)
    crime = pd.read_csv('data.csv', header=0)
    return crime



if __name__ == '__main__':
    crime = api('https://data.boston.gov/api/3/action/datastore_search?resource_id=b973d8cb-eeb2-4e7e-99da-c92938efc9c0&limit=100000')
    print(crime.dtypes)
