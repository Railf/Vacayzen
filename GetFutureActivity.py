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
df         = df[(df.start > pd.to_datetime('today').date()) | (df.end > pd.to_datetime('today').date())]

# frequency(2) => delivery first day, pickup last day
# frequency(3) => delivery and pickup each day (beach service)

activity_one = []
activity_two = []

def GetDeliveryActivity (row):
    if (row.frequency == 2):
        activity_one.append([row.start,row.category,row.asset,row.quantity,'DELIVERY'])
    else:
        period = pd.date_range(row.start,row.end,inclusive='both').date
        for day in period:
            activity_one.append([day,row.category,row.asset,row.quantity,'DELIVERY'])


def GetPickupActivity (row):
    if (row.frequency == 2):
        activity_one.append([row.end,row.category,row.asset,row.quantity,'PICKUP'])
    else:
        period = pd.date_range(row.start,row.end,inclusive='both').date
        for day in period:
            activity_one.append([day,row.category,row.asset,row.quantity,'PICKUP'])

print('getting deliveries...')
df.apply(lambda row : GetDeliveryActivity(row), axis = 1)

print('getting pickups...')
df.apply(lambda row : GetPickupActivity(row), axis = 1)


os           = pd.read_csv('/Users/workhorse/Downloads/Occupancy Staging.csv')
os.columns   = ['cid','type','unit','arrival','departure']
os.arrival   = pd.to_datetime(os.arrival).dt.date
os.departure = pd.to_datetime(os.departure).dt.date
os           = os[['unit','arrival','departure','type']]
os           = os[(os.arrival > pd.to_datetime('today').date()) | (os.departure > pd.to_datetime('today').date())]

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
                activity_two.append([row.arrival,  unit + ' - Owner','House Bike',0,'BIKE CHECK'])
                activity_two.append([row.departure,unit + ' - Departure','House Bike',0,'BIKE CHECK'])
                break
        for unit in gp:
            if unit in row.unit:
                activity_two.append([row.arrival,  unit + ' - Owner','House Gart',0,'GART CHECK'])
                activity_two.append([row.departure,unit + ' - Departure','House Gart',0,'GART CHECK'])
                break
    else:
        for unit in bp:
            if unit in row.unit:
                activity_two.append([row.departure,unit + ' - Departure','House Bike',0,'BIKE CHECK'])
                break
        for unit in gp:
            if unit in row.unit:
                activity_two.append([row.departure,unit + ' - Departure','House Gart',0,'GART CHECK'])
                break


print('getting checks...')
os.apply(lambda row : GetCheckActivity(row), axis=1)


#TODO - remove duplicates from check array
activity_two = pd.DataFrame(activity_two)
activity_two = activity_two.drop_duplicates(ignore_index=True)
activity_two.columns = ['date','category','asset','quantity','operation']
print(activity_two)


#TODO - combine activity arrays


# activity = pd.DataFrame(activity)
# activity.columns = ['date','category','asset','quantity','operation']

# print('reading in asset mapping...')
# assets = pd.read_csv('/Users/workhorse/Downloads/assets.csv')

# activity      = activity.merge(assets,'left','asset')
# activity      = activity.reset_index()
# activity.date = pd.to_datetime(activity.date).dt.date
# activity      = activity[(activity.date > pd.to_datetime('today').date()) & (activity.date < pd.to_datetime('today').date()+pd.Timedelta(days=10))]
# activity = activity[['date', 'category', 'asset', 'quantity', 'operation','department']]
# activity = activity.drop_duplicates(ignore_index=True)

# pivot = activity.pivot_table(values=['operation'],index=['date'],columns=['department'],aggfunc='count')
# pivot = pivot.fillna(0)

# pivot.to_csv('/Users/workhorse/Downloads/activity.csv')