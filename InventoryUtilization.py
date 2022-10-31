import pandas as pd

import sys

pd.options.mode.chained_assignment = None

range_start = pd.to_datetime(sys.argv[1] + ' 18:00:00')
range_end   = pd.to_datetime(sys.argv[2] + ' 18:00:00')

utilization = pd.read_csv("/Users/workhorse/Downloads/InventoryUtilization.csv", index_col=False)

inventory = pd.read_csv("/Users/workhorse/Downloads/InventoryByItem.csv", index_col=False)
inventory = dict(inventory.values)

control = utilization['RentalAgreementID'][utilization.RentalAssetMasterID == 236].values
utilization = utilization[utilization.RentalAgreementID.isin(control) == False]
utilization = utilization[utilization.RentalAgreementID != 33793] # ANOTHER CONTROL AGREEMENT

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

max_utilization_by_asset = []

for asset in utilization_by_date.index.unique():
    temp = utilization_by_date[utilization_by_date.index == asset]
    temp = temp[temp.quantity == temp.quantity.max()]

    max_utilization_by_asset.append(temp)

max_utilization = pd.concat(max_utilization_by_asset)
max_utilization['delta'] = -1 * (max_utilization.inventory - max_utilization.quantity)
# max_utilization.sort_values(by='need',ascending=False,inplace=True)
max_utilization.to_csv('/Users/workhorse/Downloads/max_utilization.csv')