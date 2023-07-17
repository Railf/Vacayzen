import pandas as pd
import numpy as np

import sys

date = pd.to_datetime(sys.argv[1])

df          = pd.read_excel('/Users/workhorse/Downloads/Availability_RAL.xlsx')
df.columns  = ['start','end','asset','quantity','type']


print('converting dates...')
df['start'] = pd.to_datetime(df['start']).dt.normalize()
df['end']   = pd.to_datetime(df['end']).dt.normalize()

print('grabbing lines that start and end on provided date...')
pickups    = df[df['end'] == date]
deliveries = df[df['start'] == date]

pickups    = pickups.pivot_table(values=['quantity'], index=['asset'], aggfunc=np.sum)
deliveries = deliveries.pivot_table(values=['quantity'], index=['asset'], aggfunc=np.sum)

pickups.columns    = ['pickups']
deliveries.columns = ['deliveries']


df = pd.merge(pickups, deliveries, on='asset')

df['need in addition to pickups to deliver'] = df.deliveries - df.pickups
df['need in addition to pickups to deliver'].clip(lower=0, inplace=True)

# print(df)

df.to_csv('/Users/workhorse/Downloads/deliveries_and_pickups.csv')