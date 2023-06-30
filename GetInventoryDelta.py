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



print('reading in counts...')
wh          = pd.read_csv('/Users/workhorse/Downloads/Vacayzen Inventory Count - Warehouse.csv')
ss          = pd.read_csv('/Users/workhorse/Downloads/Vacayzen Inventory Count - Seagrove.csv')
tp          = pd.read_csv('/Users/workhorse/Downloads/Vacayzen Inventory Count - Pointe.csv')
hb          = pd.read_csv('/Users/workhorse/Downloads/Vacayzen Inventory Count - House Bikes.csv')

print('merging counts...')
wh.columns  = ['category','asset','warehouse']
ss.columns  = ['category','asset','seagrove']
tp.columns  = ['category','asset','pointe']
hb.columns  = ['category','asset','house']

df = pd.merge(wh, ss, how='outer')
df = pd.merge(df, tp, how='outer')
df = pd.merge(df, hb, how='outer')
df = df.fillna(0)
df['counted'] = df.warehouse + df.seagrove + df.pointe + df.house
df = df[['category','asset','counted']]

print('merging rented and counted...')
total           = pd.merge(df, rented, how='left', on='asset')
total.columns   = ['category','asset','counted','rented']

print('determing total, buffer, and final quantities...')
total           = total.fillna(0)
total['total']  = total.counted + total.rented
total['buffer'] = total.total * 0.05
total           = total.round(0)
total['final']  = total.total - total.buffer

print('separating house and rental items...')
rentals = total[total.category != 'House Bikes']
house   = total[total.category == 'House Bikes']


print('reading in inventory...')
df          = pd.read_excel('/Users/workhorse/Downloads/Inventory.xlsx')
df.columns  = ['category','asset','current']
df          = df[['asset','current']]

print('merging totals and inventory...')
rental_delta          = pd.merge(rentals, df, how='left', on='asset')
rental_delta['delta'] = rental_delta.current - rental_delta.final
house_delta           = pd.merge(house, df, how='left', on='asset')
house_delta['delta']  = house_delta.current - house_delta.final



print('generating delta details...')
rental_delta.to_csv('/Users/workhorse/Downloads/rental_delta_detail.csv', index=False)
house_delta.to_csv('/Users/workhorse/Downloads/house_delta_detail.csv', index=False)

print('generating deltas...')
rd = rental_delta[['asset','delta']]
hd = house_delta[['asset','delta']]

rd = rd[rd.delta != 0]
hd = hd[hd.delta != 0]

rd.to_csv('/Users/workhorse/Downloads/rental_delta.csv', index=False)
hd.to_csv('/Users/workhorse/Downloads/house_delta.csv', index=False)
