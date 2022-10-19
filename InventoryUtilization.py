import pandas as pd

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
    print(day.date())
    temp = utilization[(utilization.start <= day) & (utilization.end >= day)]
    temp = temp.groupby('asset').sum()
    temp['date'] = day
    temp['inventory'] = temp.index.map(inventory)
    temp['utilization'] = temp['quantity'] / temp['inventory']

    inventory_by_date.append(temp)

utilization_by_date = pd.concat(inventory_by_date)
utilization_by_date.to_csv('/Users/workhorse/Downloads/utilization_by_date.csv')


max_utilization_by_asset = []

for asset in utilization_by_date.index.unique():
    print(asset)
    temp = utilization_by_date[utilization_by_date.index == asset]
    temp = temp[temp.quantity == temp.quantity.max()]

    max_utilization_by_asset.append(temp)

max_utilization = pd.concat(max_utilization_by_asset)
max_utilization.to_csv('/Users/workhorse/Downloads/max_utilization.csv')


zero_to_fourty_nine = max_utilization[max_utilization.utilization < 0.5]
zero_to_fourty_nine.to_csv('/Users/workhorse/Downloads/max_1_zero_to_fourty_nine.csv')

fifty_to_seventy_four = max_utilization[(max_utilization.utilization >= 0.5) & (max_utilization.utilization < 0.75)]
fifty_to_seventy_four.to_csv('/Users/workhorse/Downloads/max_2_fifty_to_seventy_four.csv')

seventy_five_to_eighty_nine = max_utilization[(max_utilization.utilization >= 0.75) & (max_utilization.utilization < 0.9)]
seventy_five_to_eighty_nine.to_csv('/Users/workhorse/Downloads/max_3_seventy_five_to_eighty_nine.csv')

ninety_and_up = max_utilization[max_utilization.utilization >= 0.9]
ninety_and_up.to_csv('/Users/workhorse/Downloads/max_4_ninety_and_up.csv')