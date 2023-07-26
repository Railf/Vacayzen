import pandas as pd
import numpy as np

df         = pd.read_csv('/Users/workhorse/Downloads/AgreementLines.csv')
df.columns = ['stage','type','start','end','category','asset','quantity','frequency','isRAB']
df         = df[df.stage != 'Cancel']
df         = df[df.type != 'Quote']
df         = df[df.start.notna()]
df         = df[df.end.notna()]
df         = df[df.isRAB == True]
df         = df[['start','end','category','asset','quantity','frequency']]
df.start   = pd.to_datetime(df.start).dt.date
df.end     = pd.to_datetime(df.end).dt.date

# frequency(2) => delivery first day, pickup last day
# frequency(3) => delivery and pickup each day (beach service)

activity = []

def GetDeliveryActivity (row):
    if (row.frequency == 2):
        activity.append([row.start,row.category,row.asset,row.quantity,'DELIVERY'])
    else:
        period = pd.date_range(row.start,row.end,inclusive='both').date
        for day in period:
            activity.append([day,row.category,row.asset,row.quantity,'DELIVERY'])


def GetPickupActivity (row):
    if (row.frequency == 2):
        activity.append([row.end,row.category,row.asset,row.quantity,'PICKUP'])
    else:
        period = pd.date_range(row.start,row.end,inclusive='both').date
        for day in period:
            activity.append([day,row.category,row.asset,row.quantity,'PICKUP'])

print('getting deliveries...')
df.apply(lambda row : GetDeliveryActivity(row), axis = 1)

print('getting pickups...')
df.apply(lambda row : GetPickupActivity(row), axis = 1)

activity = pd.DataFrame(activity)
activity.columns = ['date','category','asset','quantity','operation']

print('reading in asset mapping...')
assets = pd.read_csv('/Users/workhorse/Downloads/assets.csv')

activity = activity.merge(assets,'left','asset')
activity = activity.reset_index()

pivot = activity.pivot_table(values=['quantity'],index=['date'],columns=['department'],aggfunc='count')
pivot = pivot.fillna(0)

pivot.to_csv('/Users/workhorse/Downloads/activity.csv')