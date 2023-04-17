import pandas as pd

partners = pd.read_csv("/Users/workhorse/Downloads/partners.csv")
erp      = pd.read_excel("/Users/workhorse/Downloads/CTLL_ERPCustomer.xlsx")
cst      = pd.read_excel("/Users/workhorse/Downloads/CTLL_CustomerShipTo.xlsx")
ras      = pd.read_excel("/Users/workhorse/Downloads/CTLL_RentalAgreement.xlsx")

print(cst.describe)
cst = cst[cst.Status == 1]
print(cst.describe)

# df = pd.merge(erp, cst,      left_on="ID",                     right_on="ERPCustomerID")
# df = pd.merge(df,  partners, left_on="CustomerNumber",         right_on="CID")
# df = pd.merge(df,  ras,      left_on=["Latitude","Longitude"], right_on=["AgrmtJobAddrLat","AgrmtJobAddrLong"])

# print(df)