import pandas as pd
import numpy as np

da  = pd.read_csv('/Users/workhorse/Downloads/dbo_RentalDispatchActivity.csv')
t2d = pd.read_csv('/Users/workhorse/Downloads/TruckToDepartment.csv')

da = da[['Dispatch','DeliverOrPickupToType','DeliveryResource']]
da['Dispatch'] = pd.to_datetime(da['Dispatch']).dt.normalize()

da = da[da.Dispatch >= '01/01/2022']

da.columns = ['date','stops','routes']
da         = da.dropna()

da[['truck','truck_date','truck_count']] = da.routes.str.split('.', expand=True)

da     = pd.merge(da, t2d, on='truck')

stops  = da.pivot_table(values=['stops'], index=['date'], columns=['department'], aggfunc='count')
stops  = stops.reset_index()
stops  = stops.fillna(0)

routes = da.pivot_table(values=['routes'], index=['date'], columns=['department'], aggfunc=pd.Series.nunique)
routes = routes.reset_index()
routes = routes.fillna(0)

result = pd.merge(stops,routes, on='date')

result.to_csv('/Users/workhorse/Downloads/activity.csv', index=False)