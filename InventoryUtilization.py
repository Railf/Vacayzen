import pandas as pd
# import streamlit as st

import sys

pd.options.mode.chained_assignment = None

range_start = pd.to_datetime(sys.argv[1])
range_end   = pd.to_datetime(sys.argv[2])

utilization = pd.read_csv("/Users/workhorse/Downloads/InventoryUtilization.csv", index_col=False)

inventory = pd.read_csv("/Users/workhorse/Downloads/InventoryByItem.csv", index_col=False)
inventory = dict(inventory.values)

control = utilization[(utilization.RentalAssetMasterID == 236)].index
utilization.drop(control,inplace=True)

utilization = utilization[['Description','Quantity','StartDate','EndDate']]

utilization.columns = ['asset','quantity','start','end']

utilization['start'] = pd.to_datetime(utilization['start'])
utilization['end']   = pd.to_datetime(utilization['end'])

date_range = pd.date_range(range_start, range_end)


inventory_by_date = []

for day in date_range:
    temp = utilization[(utilization.start <= day) & (utilization.end >= day)]
    temp = temp.groupby('asset').sum()
    temp['date'] = day
    temp['inventory'] = temp.index.map(inventory)
    temp['utilization'] = temp['quantity'] / temp['inventory']

    inventory_by_date.append(temp)

utilization_by_date = pd.concat(inventory_by_date)
utilization_by_date.to_csv('/Users/workhorse/Downloads/utilization_by_date.csv')

buckets = []

ten = utilization_by_date[utilization_by_date.utilization < 0.1]
ten['bucket'] = '10'
buckets.append(ten)

twenty = utilization_by_date[(utilization_by_date.utilization >= 0.1) & (utilization_by_date.utilization < 0.2)]
twenty['bucket'] = '20'
buckets.append(twenty)

thirty = utilization_by_date[(utilization_by_date.utilization >= 0.2) & (utilization_by_date.utilization < 0.3)]
thirty['bucket'] = '30'
buckets.append(thirty)

forty = utilization_by_date[(utilization_by_date.utilization >= 0.3) & (utilization_by_date.utilization < 0.4)]
forty['bucket'] = '40'
buckets.append(forty)

fifty = utilization_by_date[(utilization_by_date.utilization >= 0.4) & (utilization_by_date.utilization < 0.5)]
fifty['bucket'] = '50'
buckets.append(fifty)

sixty = utilization_by_date[(utilization_by_date.utilization >= 0.5) & (utilization_by_date.utilization < 0.6)]
sixty['bucket'] = '60'
buckets.append(sixty)

seventy = utilization_by_date[(utilization_by_date.utilization >= 0.6) & (utilization_by_date.utilization < 0.7)]
seventy['bucket'] = '70'
buckets.append(seventy)

eighty = utilization_by_date[(utilization_by_date.utilization >= 0.7) & (utilization_by_date.utilization < 0.8)]
eighty['bucket'] = '80'
buckets.append(eighty)

ninty = utilization_by_date[(utilization_by_date.utilization >= 0.8) & (utilization_by_date.utilization < 0.9)]
ninty['bucket'] = '90'
buckets.append(ninty)

hundred = utilization_by_date[(utilization_by_date.utilization >= 0.9) & (utilization_by_date.utilization < 1)]
hundred['bucket'] = '100'
buckets.append(hundred)

excess = utilization_by_date[utilization_by_date.utilization >= 1]
excess['bucket'] = 'EXCESS'
buckets.append(excess)

utilization_by_bucket = pd.concat(buckets)

utilization_by_bucket.to_csv('/Users/workhorse/Downloads/utilization_by_bucket.csv')

# max_utilization_by_asset = []

# for asset in utilization_by_date.index.unique():
#     print(asset)
#     temp = utilization_by_date[utilization_by_date.index == asset]
#     temp = temp[temp.quantity == temp.quantity.max()]

#     max_utilization_by_asset.append(temp)

# max_utilization = pd.concat(max_utilization_by_asset)
# max_utilization.to_csv('/Users/workhorse/Downloads/max_utilization.csv')

# zero_to_fourty_nine = max_utilization[max_utilization.utilization < 0.5]
# zero_to_fourty_nine.to_csv('/Users/workhorse/Downloads/max_1_zero_to_fourty_nine.csv')

# fifty_to_seventy_four = max_utilization[(max_utilization.utilization >= 0.5) & (max_utilization.utilization < 0.75)]
# fifty_to_seventy_four.to_csv('/Users/workhorse/Downloads/max_2_fifty_to_seventy_four.csv')

# seventy_five_to_eighty_nine = max_utilization[(max_utilization.utilization >= 0.75) & (max_utilization.utilization < 0.9)]
# seventy_five_to_eighty_nine.to_csv('/Users/workhorse/Downloads/max_3_seventy_five_to_eighty_nine.csv')

# ninety_and_up = max_utilization[max_utilization.utilization >= 0.9]
# ninety_and_up.to_csv('/Users/workhorse/Downloads/max_4_ninety_and_up.csv')