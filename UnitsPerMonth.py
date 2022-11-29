import pandas as pd

import sys

pd.options.mode.chained_assignment = None

df = pd.read_csv("/Users/workhorse/Downloads/ppr.csv", index_col=False)

df.columns = [
    'partner','property','payment',
    'bikes','bike_type','bike_start','bike_end',
    'garts','gart_type','gart_start','gart_end',
    'sets','set_start','set_end',
    'pelotons','peloton_start','peloton_end'
    ]

df = df[df['payment'] == 'Monthly']

bikes    = df[['partner','property','bikes','bike_type','bike_start','bike_end']]
garts    = df[['partner','property','garts','gart_type','gart_start','gart_end']]
sets     = df[['partner','property','sets','set_start','set_end']]
pelotons = df[['partner','property','pelotons','peloton_start','peloton_end']]

bikes.columns    = ['partners','property','units','type','start','end']
garts.columns    = ['partners','property','units','type','start','end']
sets.columns     = ['partners','property','units','start','end']
pelotons.columns = ['partners','property','units','start','end']

categories = [bikes, garts, sets, pelotons]

for category in categories:
    category['start'] = pd.to_datetime(category['start'])
    category['end']   = pd.to_datetime(category['end'])
    category = category[category.start.isna()]



for category in categories:
    name = [x for x in globals() if globals()[x] is category][0]
    path = "/Users/workhorse/Downloads/" + name + ".csv"
    category.to_csv(path)