"""
Created on Thu Mar 23 22:31:31 2023

@author: sreed
"""

import requests
import csv
import pandas as pd
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt


#from sklearn.model_selection import train_test_split


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

def culmap(data,typeofcrime):
    try:
        crime = data[data['OFFENSE_DESCRIPTION'] == 'PROPERTY - FOUND']
        BBox = (crime.Long.min(),crime.Long.max(),crime.Lat.min(), crime.Lat.max())
        url = "https://i.ibb.co/bF1mXdX/map.png"
        urllib.request.urlretrieve(url, "map.png")
        ruh_m = Image.open(r"map.png")
        fig, ax = plt.subplots(figsize = (9,7))
        ax.scatter(crime.Long, crime.Lat, zorder=1, alpha= 0.2, c='b', s=10)
        ax.set_title('Plotting Crime Data on Boston Map')
        ax.set_xlim(BBox[0],BBox[1])
        ax.set_ylim(BBox[2],BBox[3])
        return ax.imshow(ruh_m, zorder=0, extent = BBox, aspect= 'equal')
    except:
        print("An error has occured,Please check the dataset and the offense_description provided!!!")



def fill_missing_values(df, column, fill_method):
  
    if fill_method == 'mode':
        fill_value = df[column].mode()[0]
    elif fill_method == 'median':
        fill_value = df[column].median()
    elif fill_method == 'mean':
        fill_value = df[column].mean()
    elif fill_method == 'ffill':
        fill_value = None  # use default value of fillna
    elif fill_method == 'bfill':
        fill_value = None  # use default value of fillna
    else:
        raise ValueError("Invalid fill method: {}".format(fill_method))

    df[column] = df[column].fillna(fill_value)
    return df



if __name__ == '__main__':
    crime = api('https://data.boston.gov/api/3/action/datastore_search?resource_id=b973d8cb-eeb2-4e7e-99da-c92938efc9c0&limit=100000')
    print(crime.dtypes)
