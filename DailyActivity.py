import pandas as pd


def build_summary(row):
    return f'({row.Quantity}) {row.Asset}'


df            = pd.read_csv("/Users/workhorse/Downloads/Daily Activity.csv", index_col=False)
df            = df[pd.isna(df.RentalStage)]
df            = df[~pd.isna(df.Start)]
df            = df[~pd.isna(df.End)]

df.Start      = pd.to_datetime(df.Start).dt.date
df.End        = pd.to_datetime(df.End).dt.date

today         = pd.to_datetime('today').date()
df            = df[df.Start == today]

df.Product    = df.Product.str.upper()
ignore        = ['BONFIRES', 'BEACH SERVICES', 'RENT', 'ADVENTURES', 'SEASONAL BEACH SERVICE', 'SERVICE FEE', 'CHARTER FISHING', 'BEACH SERVICES:CONTRACTED BEACH SERVICE']
df            = df[~df.Product.isin(ignore)]

df['Summary'] = df.apply(build_summary, axis=1)
df            = df.drop(columns=['Product', 'Asset', 'Quantity', 'RentalStage'])

df            = df.groupby(['Order','Start','End','Address','Unit'],dropna=False)['Summary'].agg(lambda x: '\n'.join(x)).reset_index()

df.to_csv("/Users/workhorse/Downloads/output.csv", index=False)