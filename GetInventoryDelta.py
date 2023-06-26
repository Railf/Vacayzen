import pandas as pd
import numpy as np

import sys

date = pd.to_datetime(sys.argv[1])

print('reading in availability...')
df          = pd.read_excel('/Users/workhorse/Downloads/Availability.xlsx')
df.columns  = ['start','end','asset','quantity']

print('converting dates...')
df['start'] = pd.to_datetime(df['start']).dt.normalize()
df['end']   = pd.to_datetime(df['end']).dt.normalize()

print('grabbing lines that include provided date...')
df = df[(df['start'] <= date) & (df['end'] > date)]

print('pivoting...')
rented = df.pivot_table(values=['quantity'], index=['asset'], aggfunc=np.sum)
rented = rented.reset_index()



print('reading in counted...')
df          = pd.read_csv('/Users/workhorse/Downloads/Counted.csv')
df.columns  = ['category','asset','quantity']

print('merging rented and counted...')
total           = pd.merge(df, rented, how='left', on='asset')
total.columns   = ['category','asset','counted','rented']

print('determing total, buffer, and final quantities...')
total           = total.fillna(0)
total['total']  = total.counted + total.rented
total['buffer'] = total.total * 0.05
total           = total.round(0)
total['final']  = total.total - total.buffer



print('reading in inventory...')
df          = pd.read_excel('/Users/workhorse/Downloads/Inventory.xlsx')
df.columns  = ['category','asset','current']
df          = df[['asset','current']]

print('merging total and inventory...')
delta          = pd.merge(total, df, how='left', on='asset')
delta['delta'] = delta.current - delta.final



print('generating delta_detail.csv...')
delta.to_csv('/Users/workhorse/Downloads/delta_detail.csv', index=False)

print('generating delta.csv...')
delta[['asset','delta']].to_csv('/Users/workhorse/Downloads/delta.csv', index=False)