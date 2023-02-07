import pandas as pd

df       = pd.read_csv("/Users/workhorse/Downloads/CustomerFromLatLong.csv")
partners = pd.read_csv("/Users/workhorse/Downloads/partners.csv")


df  = df.loc[df['CustomerNumber'].isin(partners.CID.values)]

out = df.merge(partners, left_on='CustomerNumber', right_on='CID').reindex(columns=['CID','Customer','PaymentDate','TransactionAmount'])

out.to_csv("/Users/workhorse/Downloads/channel_partners.csv")