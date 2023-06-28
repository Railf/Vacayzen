import pandas as pd
import numpy as np

print('reading in availability...')
df = pd.read_csv('/Users/workhorse/Downloads/Export_ExportRentalsByDay.csv', index_col=False)
df = df[['Description','Quantity','RentalAgreementStartDate', 'RentalAgreementEndDate']]
df.columns = ['access','sets','start','end']


print('converting dates...')
df['start'] = pd.to_datetime(df['start']).dt.normalize()
df['end']   = pd.to_datetime(df['end']).dt.normalize()

dates = pd.date_range(start='03/01/2023', end='10/31/2023')
setsperday  = []

for date in dates:
    sets = df[(df['start'] <= date) & (df['end'] >= date)]
    sets.columns = ['access',date,'start','end']
    sets = sets.pivot_table(values=[date], index=['access'], aggfunc=np.sum)

    setsperday.append(sets)

result = pd.concat(setsperday, axis = 1)
result = result.fillna(0)


print('generating sets.csv...')
result.to_csv('/Users/workhorse/Downloads/SetsPerAccessPerDay.csv')