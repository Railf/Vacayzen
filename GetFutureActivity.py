import pandas as pd

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


os           = pd.read_csv('/Users/workhorse/Downloads/Occupancy Staging.csv')
os.columns   = ['cid','type','unit','arrival','departure']
os.arrival   = pd.to_datetime(os.arrival).dt.date
os.departure = pd.to_datetime(os.departure).dt.date
os           = os[['unit','arrival','departure','type']]

bp = pd.read_csv('/Users/workhorse/Downloads/Partner Program Register (PPR) - BIKE.csv')
bp = bp[['PROPERTY \nCODE']]
bp.columns = ['unit']
bp = bp['unit'].values

gp = pd.read_csv('/Users/workhorse/Downloads/Partner Program Register (PPR) - GART.csv')
gp = gp[['PROPERTY \nCODE']]
gp.columns = ['unit']
gp = gp['unit'].values


def GetCheckActivity (row):
    if (row.type == 'Owner'):
        for unit in bp:
            if unit in row.unit:
                activity.append([row.arrival,  'Bikes','House Bike',0,'BIKE CHECK'])
                activity.append([row.departure,'Bikes','House Bike',0,'BIKE CHECK'])
        for unit in gp:
            if unit in row.unit:
                activity.append([row.arrival,  'Garts','House Gart',0,'GART CHECK'])
                activity.append([row.departure,'Garts','House Gart',0,'GART CHECK'])
    else:
        for unit in bp:
            if unit in row.unit:
                activity.append([row.departure,'Bikes','House Bike',0,'BIKE CHECK'])
        for unit in gp:
            if unit in row.unit:
                activity.append([row.departure,'Garts','House Gart',0,'GART CHECK'])



print('getting checks...')
os.apply(lambda row : GetCheckActivity(row), axis=1)

activity = pd.DataFrame(activity)
activity.columns = ['date','category','asset','quantity','operation']

print('reading in asset mapping...')
assets = pd.read_csv('/Users/workhorse/Downloads/assets.csv')

activity = activity.merge(assets,'left','asset')
activity = activity.reset_index()

activity.to_csv('/Users/workhorse/Downloads/activity.csv')

# pivot = activity.pivot_table(values=['quantity'],index=['date'],columns=['department'],aggfunc='count')
# pivot = pivot.fillna(0)

# pivot.to_csv('/Users/workhorse/Downloads/activity.csv')