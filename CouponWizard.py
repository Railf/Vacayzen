import pandas as pd
import numpy as np

print('reading in rental agreement lines...')
ral = pd.read_excel('/Users/workhorse/Downloads/dbo_RentalAgreementLines.xlsx')

print('reading in coupon details...')
cpd = pd.read_excel('/Users/workhorse/Downloads/dbo_CouponDetails.xlsx')

cpd['UseDate'] = pd.to_datetime(cpd['UseDate'])

today = pd.to_datetime('today').normalize()
year = pd.to_datetime('01/01/' + str(today.year)).normalize()

print('narrowing down coupon results...')
coupon = cpd[(cpd.RentalAgreementID.notnull())]
coupon = coupon[(coupon.CouponCode.str.contains('B30A'))]
coupon = coupon[(coupon.UseDate >= year)]
coupon = coupon[['CouponCode', 'UseDate', 'RentalAgreementID', 'Amount_Avl_For_Discount', 'DiscountTotal']]
coupon.columns = ['Coupon', 'Used', 'RentalAgreementID', 'Amount', 'Discount']
coupon['Guest Balance'] = coupon['Amount'] - coupon['Discount']
coupon = coupon.reset_index(drop=True)

print('generating financials...')
coupon.to_csv('/Users/workhorse/Downloads/coupon_financals.csv')
finance = coupon.pivot_table(values=['Guest Balance'], index=['Coupon'], aggfunc=np.sum)
finance = finance.reset_index()

orders = coupon[['Coupon', 'RentalAgreementID']]

orders = pd.merge(orders, ral, how='left')

print('narrowing down rental agreement line results...')
orders = orders[(orders.Product.notnull())]
orders = orders[['Coupon', 'RentalAgreementID', 'Product', 'Quantity', 'LineTotal']]
orders = orders[((orders.Product != 'Rent') & (orders.Product != 'Rental Credit') & (orders.Product != 'Service Fee'))]
orders.columns = ['Coupon', 'RentalAgreementID', 'Product', 'Quantity', 'Total']
orders = orders.reset_index(drop=True)

print('generating utilization...')
orders.to_csv('/Users/workhorse/Downloads/coupon_utilization.csv')
utilization = orders.pivot_table(values=['Quantity'], index=['Coupon'], columns=['Product'], aggfunc=np.sum)
utilization = utilization.reset_index()

print('generating product summary...')
products = orders[(orders.Total != 0)]
products = products.pivot_table(values=['Quantity', 'Total'], index=['Product'], aggfunc=np.sum)
products = products.reset_index()
products.to_csv('/Users/workhorse/Downloads/products_summary.csv', index=False)

results = pd.merge(finance, utilization, on='Coupon')
results = results.reset_index(drop=True)

print('generating coupon summary...')
results.to_csv('/Users/workhorse/Downloads/coupon_summary.csv', index=False)