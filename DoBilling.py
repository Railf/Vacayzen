import pandas as pd

import sys

pd.options.mode.chained_assignment = None

start_date = pd.to_datetime(sys.argv[1])
end_date   = pd.to_datetime(sys.argv[2])

df = pd.read_csv("/Users/workhorse/Downloads/main.csv")

print(df.columns)

# df["BIKE START DATE"] = pd.to_datetime(df["BIKE START DATE"])
# df["BIKE END DATE"]   = pd.to_datetime(df["BIKE END DATE"])

# df["COMP START DATE"] = pd.to_datetime(df["COMP START DATE"])
# df["COMP END DATE"]   = pd.to_datetime(df["COMP END DATE"])

# df["GART START DATE"] = pd.to_datetime(df["GART START DATE"])
# df["GART END DATE"]   = pd.to_datetime(df["GART END DATE"])

# df["PELOTON START DATE"] = pd.to_datetime(df["PELOTON START DATE"])
# df["PELOTON END DATE"]   = pd.to_datetime(df["PELOTON END DATE"])


# # started before the end of the period
# # ended after the start of the period, or not end

# relevant = df[(df.start < end_date) & ((df.end >= start_date) | (df.end.isna()))]

# for row in relevant.index:
#     if relevant.at[row, "start"] < start_date: relevant.at[row, "start"] = start_date
#     if relevant.at[row, "end"] > end_date:     relevant.at[row, "end"]   = end_date
#     if pd.isna(relevant.at[row, "end"]):       relevant.at[row, "end"]   = end_date

# relevant = relevant.sort_values("type")
# relevant.to_csv("/Users/workhorse/Downloads/results.csv")