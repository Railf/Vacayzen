import pandas as pd

# Homework

partners               = pd.read_csv('/Users/workhorse/Downloads/partners.csv')
sites                  = pd.read_csv('/Users/workhorse/Downloads/site_to_partner.csv')
houseAgreements        = pd.read_csv('/Users/workhorse/Downloads/house_agreements.csv')
partnerSiteAgreements  = pd.read_excel('/Users/workhorse/Downloads/CTLL_PartnerSiteRentalAgreements.xlsx')
ral                    = pd.read_excel('/Users/workhorse/Downloads/CTLL_RentalAgreementLines.xlsx')
ra                     = pd.read_excel('/Users/workhorse/Downloads/CTLL_RentalAgreement.xlsx')
pp                     = pd.read_excel('/Users/workhorse/Downloads/Prepayment Export.xlsx')


#################################################
#
# Revenue KPI
#
#################################################


# Define House Agreement Versus Rental Agreement

houseAgreements.sort_values(by=['RentalAgreementID'])

house  = ral[ral['RentalAgreementID'].isin(houseAgreements.RentalAgreementID.array)]
rental = ral[~ral['RentalAgreementID'].isin(houseAgreements.RentalAgreementID.array)]


# House Agreement (Lat, Long) => Partner

df           = house[['CustomerNumber','Latitude','Longitude']]
df           = df[df['CustomerNumber'].isin(partners.CID.array)]
df           = df.drop_duplicates()
ra2c         = pd.merge(df, ra, left_on=['Latitude','Longitude'], right_on=['AgrmtJobAddrLat', 'AgrmtJobAddrLong'], how="left")
ra2c         = ra2c.drop_duplicates(keep="last")
ra2c         = ra2c[ra2c != 0]
ra2c         = ra2c.dropna(subset=['AgrmtJobAddrLat','AgrmtJobAddrLong'])
ra2c         = ra2c[['ID','CustomerNumber']]
ra2c.columns = ['RentalAgreementNo','Partner']


# Partner Site Submission Rental Agreement (Lat, Long) => Partner

siteToPartner      = pd.merge(partners, sites, on="CID")
partnerSiteLatLong = pd.merge(partnerSiteAgreements, ra, on="ID", how="left")
partnerToLatLong   = pd.merge(partnerSiteLatLong, siteToPartner, on="OriginSource", how="left")
partnerToLatLong   = partnerToLatLong[['CID','AgrmtJobAddrLat','AgrmtJobAddrLong']]
partnerToLatLong   = partnerToLatLong.drop_duplicates(keep="last")
ra2p               = pd.merge(partnerToLatLong, ra, left_on=['AgrmtJobAddrLat', 'AgrmtJobAddrLong'], right_on=['AgrmtJobAddrLat', 'AgrmtJobAddrLong'], how="left")
ra2p               = ra2p.drop_duplicates(keep="last")
ra2p               = ra2p[ra2p != 0]
ra2p               = ra2p.dropna(subset=['AgrmtJobAddrLat','AgrmtJobAddrLong'])
ra2p               = ra2p[['ID','CID']]
ra2p.columns       = ['RentalAgreementNo','Partner']


# Combine (House Agreement (Lat, Long) => Partner) & (Partner Site Submission Rental Agreement (Lat, Long) => Partner)

ra2p = pd.concat([ra2c, ra2p])
ra2p.drop_duplicates()

# Generate Results

result          = pd.merge(pp, ra2p, how='left')
result          = result.drop_duplicates(subset=['RentalAgreementNo','RentalAgreementStartDate','RentalAgreementEndDate','RentalAgreementReservationStartDate','RentalAgreementReservationEndDate','TransactionAmount','PaymentDate','PaymentMethod'],keep='last')
result          = pd.merge(result, partners, left_on="Partner", right_on="CID", how="left")

result['RentalAgreementStartDate']            = pd.to_datetime(result['RentalAgreementStartDate']).dt.normalize()
result['RentalAgreementEndDate']              = pd.to_datetime(result['RentalAgreementEndDate']).dt.normalize()
result['RentalAgreementReservationStartDate'] = pd.to_datetime(result['RentalAgreementReservationStartDate']).dt.normalize()
result['RentalAgreementReservationEndDate']   = pd.to_datetime(result['RentalAgreementReservationEndDate']).dt.normalize()
result['PaymentDate']                         = pd.to_datetime(result['PaymentDate']).dt.normalize()

result = result.drop(columns=['Partner','CID'])

result.to_csv('/Users/workhorse/Downloads/prepayments.csv', index=False)


#################################################
#
# Activity KPI
#
#################################################

