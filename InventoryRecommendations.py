import pandas as pd

df = pd.read_excel("/Users/workhorse/Downloads/Inventory Adjustments.xlsx")

df.columns = ['asset','transaction','amount','date']

df['date'] = pd.to_datetime(df['date'])

df.sort_values(by='date')

range = pd.date_range(df.date.iloc[0],df.date.iloc[-1])

assets = pd.DataFrame(df.asset)

for date in range:
    temp = df[df.date == date]