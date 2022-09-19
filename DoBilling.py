import pandas as pd

import sys

pd.options.mode.chained_assignment = None

start_date = pd.to_datetime(sys.argv[1])
end_date   = pd.to_datetime(sys.argv[2])

df = pd.read_csv("/Users/workhorse/Downloads/main.csv", index_col=False)


df.columns = [
    'sort', 'partner', 'code', 'note', 'name', 'area', 'address', 'order', 'payment',
    'bike_count', 'bike_type', 'bike_lock', 'bike_storage', 'bike_start', 'bike_end',
    'beach_sort', 'beach_count', 'beach_label', 'beach_area', 'beach_access', 'beach_notes', 'beach_storage', 'beach_start', 'beach_end',
    'gart_count', 'gart_type', 'gart_storage', 'gart_number', 'gart_lock', 'gart_plate', 'gart_vin', 'gart_waiver', 'gart_start', 'gart_end',
    'peloton_count', 'peloton_storage', 'peloton_wifi_name', 'peloton_wifi_password', 'peloton_start', 'peloton_end'
    ]

df['bike_start']    = pd.to_datetime(df['bike_start'])
df['bike_end']      = pd.to_datetime(df['bike_end'])
df['beach_start']   = pd.to_datetime(df['beach_start'])
df['beach_end']     = pd.to_datetime(df['beach_end'])
df['gart_start']    = pd.to_datetime(df['gart_start'])
df['gart_end']      = pd.to_datetime(df['gart_end'])
df['peloton_start'] = pd.to_datetime(df['peloton_start'])
df['peloton_end']   = pd.to_datetime(df['peloton_end'])

bike = df[[
    'sort', 'partner', 'code', 'note', 'name', 'area', 'address', 'order', 'payment',
    'bike_count', 'bike_type', 'bike_lock', 'bike_storage', 'bike_start', 'bike_end'
]]

beach = df[[
    'sort', 'partner', 'code', 'note', 'name', 'area', 'address', 'order', 'payment',
    'beach_sort', 'beach_count', 'beach_label', 'beach_area', 'beach_access', 'beach_notes', 'beach_storage', 'beach_start', 'beach_end'
]]

gart = df[[
    'sort', 'partner', 'code', 'note', 'name', 'area', 'address', 'order', 'payment',
    'gart_count', 'gart_type', 'gart_storage', 'gart_number', 'gart_lock', 'gart_plate', 'gart_vin', 'gart_waiver', 'gart_start', 'gart_end'
]]

peloton = df[[
    'sort', 'partner', 'code', 'note', 'name', 'area', 'address', 'order', 'payment',
    'peloton_count', 'peloton_storage', 'peloton_wifi_name', 'peloton_wifi_password', 'peloton_start', 'peloton_end'
]]

bike    = bike[(bike.bike_start < end_date)          & ((bike.bike_end >= start_date)       | (bike.bike_end.isna()))]
beach   = beach[(beach.beach_start < end_date)       & ((beach.beach_end >= start_date)     | (beach.beach_end.isna()))]
gart    = gart[(gart.gart_start < end_date)          & ((gart.gart_end >= start_date)       | (gart.gart_end.isna()))]
peloton = peloton[(peloton.peloton_start < end_date) & ((peloton.peloton_end >= start_date) | (peloton.peloton_end.isna()))]

for row in bike.index:
    if bike.at[row, "bike_start"] < start_date: bike.at[row, "bike_start"] = start_date
    if bike.at[row, "bike_end"] > end_date:     bike.at[row, "bike_end"]   = end_date
    if pd.isna(bike.at[row, "bike_end"]):       bike.at[row, "bike_end"]   = end_date

bike = bike.sort_values('partner')

bike.to_csv('/Users/workhorse/Downloads/bike.csv')
# beach.to_csv('/Users/workhorse/Downloads/beach.csv')
# gart.to_csv('/Users/workhorse/Downloads/gart.csv')
# peloton.to_csv('/Users/workhorse/Downloads/peloton.csv')



# # started before the end of the period
# # ended after the start of the period, or not end

# relevant = df[(df.start < end_date) & ((df.end >= start_date) | (df.end.isna()))]



# relevant = relevant.sort_values("type")
# relevant.to_csv("/Users/workhorse/Downloads/results.csv")