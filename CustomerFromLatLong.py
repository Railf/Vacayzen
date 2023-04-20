import pandas as pd

# Homework
partners        = pd.read_csv('/Users/workhorse/Downloads/partners.csv')
houseAgreements = pd.read_csv('/Users/workhorse/Downloads/house agreements.csv')
siteAgreements  = pd.read_excel('/Users/workhorse/Downloads/CTLL_PartnerSiteRentalAgreements.xlsx')
ral             = pd.read_excel('/Users/workhorse/Downloads/CTLL_RentalAgreementLines.xlsx')
ra              = pd.read_excel('/Users/workhorse/Downloads/CTLL_RentalAgreement.xlsx')
pp              = pd.read_excel('/Users/workhorse/Downloads/Prepayment Export.xlsx')


house           = ral[ral['RentalAgreementID'].isin(houseAgreements.RentalAgreementID.array)]
rental          = ral[~ral['RentalAgreementID'].isin(houseAgreements.RentalAgreementID.array)]

df              = house[['CustomerNumber','Latitude','Longitude']]
df              = df[df['CustomerNumber'].isin(partners.CID.array)]
df              = df.drop_duplicates()

ra2c            = pd.merge(df, ra, left_on=['Latitude','Longitude'], right_on=['AgrmtJobAddrLat', 'AgrmtJobAddrLong'])
ra2c            = ra2c[['ID','CustomerNumber']]

ra2c.columns    = ['RentalAgreementNo','Partner']

result          = pd.merge(pp, ra2c, how='left')
result          = result.drop_duplicates(subset=['RentalAgreementNo','RentalAgreementStartDate','RentalAgreementEndDate','RentalAgreementReservationStartDate','RentalAgreementReservationEndDate','TransactionAmount','PaymentDate','PaymentMethod'],keep='last')

result['RentalAgreementStartDate']            = pd.to_datetime(result['RentalAgreementStartDate']).dt.normalize()
result['RentalAgreementEndDate']              = pd.to_datetime(result['RentalAgreementEndDate']).dt.normalize()
result['RentalAgreementReservationStartDate'] = pd.to_datetime(result['RentalAgreementReservationStartDate']).dt.normalize()
result['RentalAgreementReservationEndDate']   = pd.to_datetime(result['RentalAgreementReservationEndDate']).dt.normalize()
result['PaymentDate']                         = pd.to_datetime(result['PaymentDate']).dt.normalize()

result.to_csv('/Users/workhorse/Downloads/prepayments.csv', index=False)
house.to_csv('/Users/workhorse/Downloads/house_activity.csv', index=False)
rental.to_csv('/Users/workhorse/Downloads/rental_activity.csv', index=False)