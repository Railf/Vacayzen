import pandas as pd

aa = pd.read_excel('/Users/workhorse/Downloads/ActiveAssets.xlsx')
am = pd.read_excel('/Users/workhorse/Downloads/dbo_RentalAssetMaster.xlsx')

aa = aa.ID

df = pd.merge(aa,am,how='left')

print(df)

df.to_csv('/Users/workhorse/Downloads/ActiveAssetMasters.csv', index=False)