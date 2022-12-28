import pandas as pd

import sys

pd.options.mode.chained_assignment = None

range_start = pd.to_datetime(sys.argv[1] + ' 18:00:00')
range_end   = pd.to_datetime(sys.argv[2] + ' 18:00:00')

ra  = pd.read_csv("/Users/workhorse/Downloads/inventory/dbo_RentalAgreement.csv", low_memory=False)
ral = pd.read_csv("/Users/workhorse/Downloads/inventory/dbo_RentalAgreementLines.csv", low_memory=False)

ra = ra.loc[ra['RentalAgreementTypeID'].isin([1,2])]
ra = ra[ra['RentalStage'] != 'Cancel']
ra = ra[ra.RentalAgreementNo != 33793]

ral = ral.loc[ral['RentalAgreementID'].isin(ra['RentalAgreementNo'].values)]

control = ral['RentalAgreementID'][ral.RentalAssetMasterID == 236].values
ral = ral[ral.RentalAgreementID.isin(control) == False]

print(ral)