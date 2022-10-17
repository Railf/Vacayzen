import pandas as pd

import sys

pd.options.mode.chained_assignment = None

range_start = pd.to_datetime(sys.argv[1])
range_end   = pd.to_datetime(sys.argv[2])

df = pd.read_csv("/Users/workhorse/Downloads/dbo_vAvailability.csv", index_col=False)
df = df[['RentalAssetMasterID','Quantity','StartDate','EndDate','AvailabilityType']]

df.columns = ['asset','quantity','start','end','type']

df['start']    = pd.to_datetime(df['start'])
df['end']      = pd.to_datetime(df['end'])

date_range = pd.date_range(range_start, range_end)

inventory_by_date = []

for day in date_range:
    temp = df[(df.start <= day) & (df.end >= day)]
    temp = temp.groupby('asset').sum()
    temp['date'] = day

    inventory_by_date.append(temp)

utilization_by_date = pd.concat(inventory_by_date)
utilization_by_date.to_csv('/Users/workhorse/Downloads/utilization_by_date.csv')