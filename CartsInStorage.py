import pandas as pd

import sys

pd.options.mode.chained_assignment = None

range_start = pd.to_datetime(sys.argv[1])
range_end   = pd.to_datetime(sys.argv[2])
date_range  = pd.date_range(range_start, range_end)

period_rate = int(sys.argv[3])
daily_rate  = period_rate / len(date_range)

df = pd.read_csv("/Users/workhorse/Downloads/carts.csv", index_col=False)

df['added'] = pd.to_datetime(df['added'])
df['removed']   = pd.to_datetime(df['removed'])

carts_in_storage = []

for day in date_range:
    count = df[(df.added <= day) & ((df.removed > day) | (df.removed.isna()))]
    carts_in_storage.append(100 - len(count.index))

carts = pd.DataFrame(carts_in_storage)
carts.columns = ['in_storage']
carts.index += 1
carts['daily_rate'] = daily_rate
carts['daily_cost'] = carts.in_storage * carts.daily_rate
carts['date'] = date_range
carts['location']   = 'Vacayzen Warehouse'
carts['service']    = 'Storage'
carts = carts[['location','date','service','in_storage','daily_rate','daily_cost']]

carts.to_csv("/Users/workhorse/Downloads/carts_results.csv")