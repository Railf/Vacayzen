import pandas as pd

pd.options.mode.chained_assignment = None

df = pd.read_csv("/Users/workhorse/Downloads/ppr.csv", index_col=False)

df.columns = [
    'partner','property','payment',
    'bikes','bike_type','bike_start','bike_end',
    'garts','gart_type','gart_start','gart_end',
    'sets','set_start','set_end',
    'pelotons','peloton_start','peloton_end'
    ]

df = df[df['payment'] == 'Monthly']

bikes    = df[['partner','property','bikes','bike_type','bike_start','bike_end']]
garts    = df[['partner','property','garts','gart_type','gart_start','gart_end']]
sets     = df[['partner','property','sets','set_start','set_end']]
pelotons = df[['partner','property','pelotons','peloton_start','peloton_end']]

bikes.columns    = ['partner','property','units','type','start','end']
garts.columns    = ['partner','property','units','type','start','end']
sets.columns     = ['partner','property','units','start','end']
pelotons.columns = ['partner','property','units','start','end']

date_range = pd.date_range("01/01/2022","12/31/2022",freq="M")

categories = [bikes, garts, sets, pelotons]

results = []

for category in categories:
    df = category

    df['start'] = pd.to_datetime(df['start'])
    df['end']   = pd.to_datetime(df['end'])
    df = df[df.start.isna() == False]

    year = []

    for date in date_range:
        month = df[(df.start <= date) & ((df.end > date) | (df.end.isna()))]
        month = month.groupby(['partner']).sum(True)
        month.columns = [date]
        year.append(month)

    result = pd.concat(year, axis=1)
    results.append(result)

for i, result in enumerate(results):
    name = ''

    if   i == 0: name = 'bikes'
    elif i == 1: name = 'garts'
    elif i == 2: name = 'sets'
    elif i == 3: name = 'pelotons'

    file = '/Users/workhorse/Downloads/' + name + '.csv'

    result.to_csv(file)