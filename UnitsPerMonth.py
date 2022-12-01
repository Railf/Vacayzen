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

bikes.columns    = ['partner','property','units','type','start','end']
garts.columns    = ['partner','property','units','type','start','end']
sets.columns     = ['partner','property','units','start','end']
pelotons.columns = ['partner','property','units','start','end']


bikes['start'] = pd.to_datetime(bikes['start'])
bikes['end']   = pd.to_datetime(bikes['end'])
bikes = bikes[bikes.start.isna() == False]


# garts['start'] = pd.to_datetime(garts['start'])
# garts['end']   = pd.to_datetime(garts['end'])
# garts = garts[garts.start.isna() == False]

# sets['start'] = pd.to_datetime(sets['start'])
# sets['end']   = pd.to_datetime(sets['end'])
# sets = sets[sets.start.isna() == False]

# pelotons['start'] = pd.to_datetime(pelotons['start'])
# pelotons['end']   = pd.to_datetime(pelotons['end'])
# pelotons = pelotons[pelotons.start.isna() == False]

date_range = pd.date_range("01/01/2022","12/31/2022",freq="M")

year = []

df = bikes

for date in date_range:
    month = df[(df.start <= date) & ((df.end > date) | (df.end.isna()))]
    month = month.groupby(['partner']).sum(True)
    month.columns = [date]
    year.append(month)

results = pd.concat(year, axis=1)

results.to_csv('/Users/workhorse/Downloads/_bikes.csv')


# bikes.to_csv('/Users/workhorse/Downloads/_bikes.csv')
# garts.to_csv('/Users/workhorse/Downloads/_garts.csv')
# sets.to_csv('/Users/workhorse/Downloads/_sets.csv')
# pelotons.to_csv('/Users/workhorse/Downloads/_pelotons.csv')