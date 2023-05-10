import pandas as pd
import numpy as np

ral = pd.read_excel('/Users/workhorse/Downloads/dbo_RentalAgreementLines.xlsx')
cpd = pd.read_excel('/Users/workhorse/Downloads/dbo_CouponDetails.xlsx')

cpd['UseDate'] = pd.to_datetime(cpd['UseDate'])

today = pd.to_datetime('today').normalize()
year = pd.to_datetime('01/01/' + str(today.year)).normalize()

print(year)

coupon = cpd[(cpd.RentalAgreementID.notnull())]
coupon = coupon[(coupon.CouponCode.str.contains('B30A'))]
coupon = coupon[(coupon.UseDate >= year)]
coupon = coupon[['CouponCode','UseDate','RentalAgreementID','Amount_Avl_For_Discount','DiscountTotal']]
coupon.columns = ['Coupon','Used','RentalAgreementID','Amount','Discount']
coupon['Guest Balance'] = coupon['Amount'] - coupon['Discount']
coupon = coupon.reset_index(drop=True)

coupon.to_csv('/Users/workhorse/Downloads/coupon_financals.csv')
finance = coupon.pivot_table(values=['Guest Balance'], index=['Coupon'], aggfunc=np.sum)
finance = finance.reset_index()

orders = coupon[['Coupon', 'RentalAgreementID']]

orders = pd.merge(orders, ral, how='left')

orders = orders[(orders.Product.notnull())]
orders = orders[['Coupon', 'RentalAgreementID', 'Product', 'Quantity']]
orders = orders[((orders.Product != 'Rent') & (orders.Product != 'Rental Credit') & (orders.Product != 'Service Fee'))]
orders = orders.reset_index(drop=True)

orders.to_csv('/Users/workhorse/Downloads/coupon_utilization.csv')
utilization = orders.pivot_table(values=['Quantity'], index=['Coupon'], columns=['Product'], aggfunc=np.sum)
utilization = utilization.reset_index()

results = pd.merge(finance, utilization, on='Coupon')
results = results.reset_index(drop=True)

results.to_csv('/Users/workhorse/Downloads/coupon_summary.csv', index=False)