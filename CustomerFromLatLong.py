import pandas as pd

data     = pd.read_csv("/Users/workhorse/Downloads/CustomerFromLatLong.csv")
partners = pd.read_csv("/Users/workhorse/Downloads/partners.csv", index_col="CID")


print(data.columns)

test = data.loc[data['CustomerNumber'].isin(partners.index.values)]

print(test)