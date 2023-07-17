import pandas as pd
import numpy as np

import sys

date = pd.to_datetime(sys.argv[1])

av          = pd.read_excel('/Users/workhorse/Downloads/Availability_RAL.xlsx')
av.columns  = ['start','end','asset','quantity','type']

inv         = pd.read_excel('/Users/workhorse/Downloads/Inventory.xlsx')
inv.columns = ['category','asset','quantity']


print('converting dates...')
av['start'] = pd.to_datetime(av['start']).dt.normalize()
av['end']   = pd.to_datetime(av['end']).dt.normalize()

print('grabbing lines that start and end on provided date...')
rent = av[((av['start'] <= date) & (av['end'] > date)) & (av['type'] == 'Rental')]

rent.to_csv('/Users/workhorse/Downloads/test.csv')

# res  = av[((av['start'] == date)) & (av['type'] == 'Reservation')]

# rent = rent.pivot_table(values=['quantity'], index=['asset'], aggfunc=np.sum)
# res  = res.pivot_table(values=['quantity'], index=['asset'], aggfunc=np.sum)

# rent.columns = ['rented']
# res.columns  = ['reserved']


# df = pd.merge(inv, rent, on='asset', how='left')
# df = pd.merge(df, res, on='asset', how='left')
# df['utilization'] = df.rented + df.reserved

# df['available'] = df.quantity - df.utilization
# df = df[['asset','rented','reserved','available']]


# print(df)

# df.to_csv('/Users/workhorse/Downloads/rra.csv')