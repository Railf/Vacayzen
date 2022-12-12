from pathlib import Path
from glob import glob

import pandas as pd

import credentials
import webbrowser
import os
import sys

pd.options.mode.chained_assignment = None

partners = {
    '30A Luxury': [],
    '360 Blue':   [],
    'Callista':   [],
    'Dune':       [],
    'Exclusive':  [],
    'Oversee':    [],
    'Royal':      []
}


def WaitForDownload(filename, extension):
    print("downloading...")

    os.chdir(str(Path.home() / "Downloads"))

    while not glob(filename + "*." + extension): continue


webbrowser.open(credentials.Links['Partner Program Register'])
webbrowser.open(credentials.Links['Partner Billing Escapia'])

WaitForDownload('Partner Program Register - REGISTER','csv')

df = pd.read_csv("/Users/workhorse/Downloads/Partner Program Register - REGISTER.csv", index_col=False)
# billing = pd.read_csv("/Users/workhorse/Downloads/Partner Program Register - REGISTER.csv", index_col=False)

df.columns = [
    'geo','partner','property','notes','name','area','address','order','payment',
    'bike_count','bike_type','bike_lock','bike_storage','bike_start','bike_end',
    'gart_count','gart_type','gart_storage','gart_number','gart_lockbox','gart_plate','gart_vin','gart_waiver','gart_start','gart_end',
    'sets_geo','set_count','sets_tag','sets_access','sets_notes','sets_storage','set_start','set_end',
    'peloton_count','peloton_storage','peloton_wifi_name','peloton_wifi_password','peloton_start','peloton_end'
    ]

df = df[df['payment'] == 'Paid']

bikes    = df[['partner','property','bike_count','bike_type','bike_start','bike_end']]
garts    = df[['partner','property','gart_count','gart_type','gart_start','gart_end']]
sets     = df[['partner','property','set_count','set_start','set_end']]
pelotons = df[['partner','property','peloton_count','peloton_start','peloton_end']]

bikes.columns    = ['partner','property','units','type','start','end']
garts.columns    = ['partner','property','units','type','start','end']
sets.columns     = ['partner','property','units','start','end']
pelotons.columns = ['partner','property','units','start','end']

date_range = pd.date_range("01/01/2022","12/31/2022",freq="M")

categories = [bikes, garts, sets, pelotons]

results = []

for category in categories:
    df = category

    df['start'] = pd.to_datetime(df['start'])
    df['end']   = pd.to_datetime(df['end'])
    df = df[df.start.isna() == False]

    year = []

    for date in date_range:
        month = df[(df.start <= date) & ((df.end > date) | (df.end.isna()))]
        month = month.groupby(['partner']).sum(True)
        month.columns = [date]
        year.append(month)

    result = pd.concat(year, axis=1)
    results.append(result)

for i, result in enumerate(results):
    name = ''

    if   i == 0: name = 'bikes'
    elif i == 1: name = 'garts'
    elif i == 2: name = 'sets'
    elif i == 3: name = 'pelotons'

    file = '/Users/workhorse/Downloads/' + name + '.csv'

    result.to_csv(file)