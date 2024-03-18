import pandas as pd

import credentials
import sys

pd.options.mode.chained_assignment = None

date = pd.to_datetime(sys.argv[1])

df = pd.read_csv("/Users/workhorse/Downloads/Constant Contact.csv", index_col=False)

df.columns = ['contact','email','date']

df['date'] = pd.to_datetime(df['date']).dt.floor('d')

df = df[df['date'] > date]

for partner in credentials.partners:
    df = df[df['email'].str.contains(partner) == False]

df = df.sort_values('date')
df = df.drop_duplicates()
df = df.reset_index(drop=True)
df.index += 1

df.to_csv('/Users/workhorse/Downloads/contacts.csv')