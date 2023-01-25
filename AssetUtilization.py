import pandas as pd

import sys

pd.options.mode.chained_assignment = None

range_start = pd.to_datetime(sys.argv[1] + ' 18:00:00')
range_end   = pd.to_datetime(sys.argv[2] + ' 10:00:00')

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

# assets.to_csv('/Users/workhorse/Downloads/utilization_by_date.csv')
assets = assets.reset_index()

buckets = []
for i in range(1,1001,1): buckets.append(i)

groups = {}

for bucket in buckets:
    temp = assets[assets.quantity >= bucket]
    groups[bucket] = temp.groupby('asset').count()['quantity']

utilization = pd.DataFrame.from_dict(groups)
utilization = utilization.astype(float)
# results.to_csv('/Users/workhorse/Downloads/assets_by_bucket.csv')

asset_rates = pd.read_csv("/Users/workhorse/Downloads/assets.csv", index_col='asset')
asset_rates = asset_rates.dropna()
asset_rates = asset_rates.astype(float)

# CALCULATE ANNUAL REVENUE @ INVENTORY NUMBER

rows = []

for column in utilization.columns:
    rows.append(utilization[column] * asset_rates['daily_price'])

annual_revenue = pd.concat(rows,axis=1)
annual_revenue.columns += 1

# CALCULATE FIXED COST @ INVENTORY NUMBER

rows = []

for column in utilization.columns:
    rows.append(utilization[column] * 0 + asset_rates['unit_price'])

fixed_cost = pd.concat(rows,axis=1)
fixed_cost.columns += 1

# CALCULATE VARIABLE LABOR

rows = []

for column in utilization.columns:
    rows.append(utilization[column] * 0)

variable_labor = pd.concat(rows,axis=1)

# CALCULATE MARGINAL REVENUE

marginal_revenue = annual_revenue - fixed_cost - variable_labor

print('building deliverable...', end=" ")
with pd.ExcelWriter('/Users/workhorse/Downloads/recommendation.xlsx') as writer:
    utilization.to_excel(writer, sheet_name='utilization')
    asset_rates.to_excel(writer, sheet_name='asset_rates')
    annual_revenue.to_excel(writer, sheet_name='annual revenue')
    fixed_cost.to_excel(writer, sheet_name='fixed cost')
    variable_labor.to_excel(writer, sheet_name='variable labor')
    marginal_revenue.to_excel(writer, sheet_name='marginal revenue')
print('done')