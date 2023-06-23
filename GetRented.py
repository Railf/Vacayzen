import pandas as pd
import numpy as np

import sys

date = pd.to_datetime(sys.argv[1])

print('reading in availability...')
df          = pd.read_excel('/Users/workhorse/Downloads/Availability.xlsx')
df.columns  = ['status','start','end','asset','quantity']

print('converting dates...')
df['start'] = pd.to_datetime(df['start']).dt.normalize()
df['end']   = pd.to_datetime(df['end']).dt.normalize()

print('removing cancelled line items...')
df = df[df['status'].isna() == True]
df = df[['start','end','asset','quantity']]

print('grabbing lines that include provided date...')
df = df[(df['start'] <= date) & (df['end'] > date)]

print('pivoting...')
result = df.pivot_table(values=['quantity'], index=['asset'], aggfunc=np.sum)
result = result.reset_index()

print('generating rented.csv...')
result.to_csv('/Users/workhorse/Downloads/rented.csv', index=False)