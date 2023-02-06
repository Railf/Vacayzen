import pandas as pd

import sys

pd.options.mode.chained_assignment = None

range_start = pd.to_datetime(sys.argv[1] + ' 18:00:00')
range_end   = pd.to_datetime(sys.argv[2] + ' 10:00:00')

print('organizing asset data...')

df = pd.read_csv("/Users/workhorse/Downloads/AssetUtilization.csv")

## FIELDS
#  ID
#  CustomerNumber                       # != 10331
#  RentalStage                          # != 'Cancel'
#  RentalAgreementTypeID                # != 3
#  RentalAssetItemID                    # != 341, 342 
#  RentalAssetMasterID                  # != 235, 236
#  Description
#  Quantity
#  RentalAgreementReservationStartDate
#  RentalAgreementReservationEndDate

filters = []

filters.append(list(set(df.ID[df.CustomerNumber == 10331].values)))
filters.append(list(set(df.ID[df.RentalStage == 'Cancel'].values)))
filters.append(list(set(df.ID[df.RentalAgreementTypeID == 3].values)))
filters.append(list(set(df.ID[df.RentalAssetItemID == 341].values)))
filters.append(list(set(df.ID[df.RentalAssetItemID == 342].values)))
filters.append(list(set(df.ID[df.RentalAssetMasterID == 235].values)))
filters.append(list(set(df.ID[df.RentalAssetMasterID == 236].values)))

for filter in filters: df = df[df.ID.isin(filter) == False]

df          = df[['Description','Quantity','RentalAgreementReservationStartDate','RentalAgreementReservationEndDate']]
df.columns  = ['asset','quantity','start','end']
df          = df.reset_index()

print('calculating rentals per day per asset...')

df['start'] = pd.to_datetime(df['start'])
df['end']   = pd.to_datetime(df['end'])

date_range  = pd.date_range(range_start, range_end)

inventory_by_date = []

for day in date_range:
    temp = df[(df.start <= day) & (df.end >= day)]
    temp = temp.groupby('asset').sum(numeric_only=True)
    temp['date'] = day

    inventory_by_date.append(temp)

assets = pd.concat(inventory_by_date)

assets = assets[['quantity','date']]
assets.reset_index(drop=True)

assets = assets.reset_index()

assets.to_csv("/Users/workhorse/Downloads/utilization.csv")