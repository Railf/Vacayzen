from datetime import timedelta

import pandas as pd

import sys


start_date = pd.to_datetime(sys.argv[1])
end_date   = pd.to_datetime(sys.argv[2])

df = pd.read_csv("/Users/workhorse/Downloads/Export_ExportRentalsByDay.csv", index_col=False)

df.columns = ["customer","order","access","comment","sets","not_used","po_number","vendor","agent","agent_email","start","end","days","set_days"]
df = df[["customer","order","access","comment","sets","po_number","vendor","agent","agent_email","start","end","days","set_days"]]

df.start = pd.to_datetime(df.start).dt.floor('d')
df.end   = pd.to_datetime(df.end).dt.floor('d')

df = df[
    ((df.start <= start_date) & (end_date <= df.end)) |
    ((start_date <= df.start) & ((df.start <= end_date) & (end_date <= df.end))) |
    (((df.start <= start_date) & (start_date <= df.end)) & (df.end <= end_date)) |
    ((start_date <= df.start) & (df.end <= end_date))
    ]

for row in df.index:
    if df.at[row, "start"] < start_date: df.at[row, "start"] = start_date
    if df.at[row, "end"] > end_date:     df.at[row, "end"]   = end_date

df.days = (df.end - df.start + timedelta(1)).dt.days
df.set_days = df.sets * df.days

# for vendor in df.vendor.unique():
#     df[df.vendor == vendor].to_csv(f"/Users/workhorse/Downloads/{vendor}.csv")

billing = df[["vendor","set_days"]].groupby("vendor").sum()
billing = billing.reset_index()
billing["cost"] = billing["set_days"] * 23

billing.to_csv("/Users/workhorse/Downloads/billing.csv")