from datetime import datetime
from fpdf import FPDF

import credentials
import webbrowser
import csv
import sys
import os

def RunScript(script):
    status = -1
    status = os.system("python3" + " " + script + ".py")
    while status == -1: continue

def RunScriptWithArguments(script, arguments):
    command = "python3" + " " + script + ".py"

    for argument in arguments:
        command += " " + argument

    status = -1
    status = os.system(command)
    while status == -1: continue

def GetCSVFromGoogleSheetTab(sheetID,tabID):
    part0 = "https://docs.google.com/spreadsheets/d/"
    part1 = sheetID
    part2 = "/export?format=csv&gid="
    part3 = tabID

    webbrowser.open(part0 + part1 + part2 + part3)

def GetOrderDataFromCSV():
    data = []

    with open('/Users/workhorse/Downloads/Export_ExportRentalsByDay.csv') as file:
        reader = csv.reader(file)

        for row in reader:
            data.append(row[:-1])

    with open('/Users/workhorse/Downloads/SWBSA Billing Master - ONE-OFF ADDS.csv') as file:
        reader = csv.reader(file)

        for row in reader:
            data.append(row)

    return data

def GetWalkupDataFromCSV():
    data = []

    with open('/Users/workhorse/Downloads/Export_Walkups.csv') as file:
        reader = csv.reader(file)

        for row in reader:
            data.append(row[1:])

    return data

def GetConfigDataFromCSV():
    with open('/Users/workhorse/Downloads/SWBSA Billing Master - CONFIG.csv') as file:
        reader = csv.DictReader(file)

        data = list(reader)[0]
        data = dict(data)
    
    return data

def GetMemberDataFromCSV():
    data = {}
    with open('/Users/workhorse/Downloads/SWBSA Billing Master - MEMBERS.csv') as file:
        reader = csv.reader(file)

        for row in list(reader)[1:]:
            data[row[0]] = {'email': row[1], 'isTaxExempt': row[2]}
    
    return data

def GetAccessDataFromCSV():
    data = []
    with open('/Users/workhorse/Downloads/SWBSA Billing Master - ACCESSES.csv') as file:
        reader = csv.reader(file)

        for row in list(reader)[1:]:
            for cell in row:
                data.append(cell)

    return data

def ConvertOrderDates(order):
    order[4]  = int(float(order[4]))
    order[10] = datetime.strptime(order[10],"%m/%d/%Y %I:%M:%S %p")
    order[10] = datetime(order[10].year, order[10].month, order[10].day)
    order[11] = datetime.strptime(order[11],"%m/%d/%Y %I:%M:%S %p")
    order[11] = datetime(order[11].year, order[11].month, order[11].day)

    return order

def IsRelevantOrder(start, end, order):
    return ((order[10] >= start and order[10] <= end) or
            (order[11] >= start and order[11] <= end) or
            (order[10] <  start and order[11] >  end))

def SetOrderDatesToRange(start, end, order):
    if order[10] < start: order[10] = start
    if order[11] > end:   order[11] = end

    order[12] = (order[11] - order[10]).days + 1
    order[13] = order[4] * order[12]

    order[10] = order[10].strftime("%m/%d/%Y")
    order[11] = order[11].strftime("%m/%d/%Y")

    return order

def GetRelevantOrdersByRange(start, end, orders):
    setDayCount = 0
    ordersByVendor = {}
    ordersByAccess = {}

    for order in orders[1:]:
        order = ConvertOrderDates(order)

        if IsRelevantOrder(start, end, order):
            SetOrderDatesToRange(start, end, order)

            # Orders By Vendor
            if order[7] in ordersByVendor.keys():
                ordersByVendor[order[7]].append(order)
            else:
                ordersByVendor[order[7]] = [order]
            
            # Orders By Access
            if order[2] in ordersByAccess.keys():
                ordersByAccess[order[2]].append(order)
            else:
                ordersByAccess[order[2]] = [order]
            
            setDayCount += order[13]
    
    return [setDayCount, ordersByVendor, ordersByAccess]

def CreateResultsCSV(key, data):
    print("generating", key+".csv...")
    with open("/Users/workhorse/Downloads/"+key+".csv", 'w') as file:
        write = csv.writer(file)
        write.writerows(data)

def GetStatsByVendor(ordersByVendor, members, costPerSet, taxRate):
    statsByVendor = {}

    for vendor in ordersByVendor:
        if vendor not in statsByVendor: statsByVendor[vendor] = {}

        setDays     = 0
        for order in ordersByVendor[vendor]: setDays += order[13]
        isTaxExempt = members[vendor]['isTaxExempt'] == 'TRUE'
        tax         = CalculateTax(setDays, isTaxExempt, costPerSet, taxRate)

        statsByVendor[vendor]['email']       = members[vendor]['email']
        statsByVendor[vendor]['setDays']     = setDays
        statsByVendor[vendor]['costPerSet']  = float(costPerSet)
        statsByVendor[vendor]['subtotal']    = float(setDays) * float(costPerSet)
        statsByVendor[vendor]['isTaxExempt'] = isTaxExempt
        statsByVendor[vendor]['tax']         = tax
        statsByVendor[vendor]['total']       = float(float(setDays)*float(costPerSet)+float(tax))

    return statsByVendor

def GenerateVendorUtilization(statsByVendor, setDayCount, start):
    summary = [['VENDOR','MONTH','PERCENTAGE']]

    for vendor in statsByVendor:
        summary.append([
            vendor,
            start.strftime("%B").upper(),
            '{:.3%}'.format(float(statsByVendor[vendor]['setDays']/setDayCount))
            ])
    
    return summary

def GetSWBSAAcess(access):
    match access:
        case 'Andalusia Access - SoWal':           return 'ANDALUSIA'
        case 'Azalea Access- SoWal':               return 'AZALEA'
        case 'Blue Mountain Access- SoWal':        return 'BLUE MOUNTAIN'
        case 'Camelia Access- SoWal':              return 'CAMELIA'
        case 'Dothan Access- SoWal':               return 'DOTHAN'
        case 'Dune Allen-SoWal':                   return 'DUNE ALLEN REGIONAL'
        case 'Ed Walline-SoWal':                   return 'ED WALLINE'
        case 'Ft Panic-SoWal':                     return 'FORT PANIC'
        case 'Gardenia Access- SoWal':             return 'GARDENIA'
        case 'Grayton Beach Access- SoWal':        return 'GRAYTON BEACH'
        case 'Greenwood Access- SoWal':            return 'GREENWOOD'
        case 'Gulfview Heights Access- SoWal':     return 'GULFVIEW HEIGHTS'
        case 'Hickory Street Access- SoWal':       return 'HICKORY'
        case 'Holly Access- SoWal':                return 'HOLLY'
        case 'HWY 395 Access- SoWal':              return '395'
        case 'Inlet Beach Access- SoWal':          return 'INLET BEACH'
        case 'Liveoak Access- SoWal':              return 'LIVEOAK'
        case 'Nightcap Street Access- SoWal':      return 'NIGHTCAP'
        case 'One Seagrove Place Access- SoWal':   return 'ONE SEAGROVE PLACE'
        case 'Santa Clara/ Bramble Access- SoWal': return 'SANTA CLARA BRAMBLE'
        case 'Shellseekers-SoWal':                 return 'SHELLSEEKERS COVE'
        case 'Spooky Lane Access- SoWal':          return 'SPOOKY LANE'
        case 'Van Ness Bulter Access- SoWal':      return 'VAN NESS BUTLER'
        case 'Wall Street Access- SoWal':          return 'WALL STREET'
        case 'Walton Dunes Access- SoWal':         return 'WALTON DUNES'
        case 'Walton Lakeshore Access - SoWal':    return 'WALTON LAKESHORE'
        case _: return access

def MapBeachyToSWBSA(walkups):
    newData = []

    for walkup in walkups:
        walkup[0] = GetSWBSAAcess(walkup[0])
        newData.append(walkup)

    return newData

def GetRelevantWalkups(walkups):
    newData = []

    for walkup in walkups:
        if (walkup[2] == 'Beach Set' or walkup[2] == 'Beach Umbrella'):
            newData.append(walkup)
    
    return newData

def OrganizeWalkups(walkups):
    newData = {}

    for walkup in walkups:
        if walkup[0] in newData.keys():
            newData[walkup[0]] += int(walkup[3].replace(',',''))
        else:
            newData[walkup[0]]  = int(walkup[3].replace(',',''))
    
    return newData

def OrganizeOrders(ordersByAccess):
    newData = {}

    for access in ordersByAccess:
        for order in ordersByAccess[access]:
            if order[2] in newData.keys():
                newData[order[2]] += int(order[13])
            else:
                newData[order[2]]  = int(order[13])
    
    return newData

def BuildAccessSummary(summary, accesses, orders, walkups, fee):
    for access in accesses:
        if (access in orders.keys() and access in walkups.keys()):
            summary.append([access, orders[access], '$'+str(orders[access]*fee), walkups[access], '$'+str(walkups[access]*fee)])
            continue
        elif (access in orders.keys() and not access in walkups.keys()):
            summary.append([access, orders[access], '$'+str(orders[access]*fee), 0, 0])
            continue
        elif (not access in orders.keys() and access in walkups.keys()):
            summary.append([access, 0, 0, walkups[access], '$'+str(walkups[access]*fee)])
            continue
        else:
            summary.append([access, 0, 0, 0, 0])
    
    return summary

def GetNumberOfWalkups(walkups):
    count = 0

    for walkup in walkups:
        count += int(walkup[3].replace(',',''))
    
    return count

def GenerateAccessUtilization(accesses, ordersByAccess, walkups, fee, start):
    summary = [[start.strftime("%B").upper(), 'ORDERS','',      'WALKUPS',''      ],
               ['ACCESS',                     'SETS',  'COUNTY','SETS',   'COUNTY']]
    
    walkups = MapBeachyToSWBSA(walkups)
    walkups = GetRelevantWalkups(walkups)
    walkups = OrganizeWalkups(walkups)
    orders  = OrganizeOrders(ordersByAccess)

    summary = BuildAccessSummary(summary, accesses, orders, walkups, fee)

    return summary

def GenerateSummary(setDayCount, walkups, fee):
    summary = [['TYPE','SETS','COUNTY']]

    walkups = GetRelevantWalkups(walkups)
    walkups = GetNumberOfWalkups(walkups)

    summary.append(['ORDERS', setDayCount,         '$'+str(setDayCount*fee)])
    summary.append(['WALKUPS',walkups,             '$'+str(walkups*fee)])
    summary.append(['',       setDayCount+walkups, '$'+str((setDayCount+walkups)*fee)])

    return summary

def CalculateTax(setDays, isTaxExempt, costPerSet, taxRate):
    if isTaxExempt:
        return float(0)

    tax = float(setDays) * float(costPerSet) * float(taxRate)
    
    return tax

def GenerateBillingSummary(statsByVendor):
    summary = [['VENDOR','EMAIL','SETS','COST PER','VENDOR COST','TAX EXEMPT?','TAX','TOTAL']]

    for vendor in statsByVendor:
        email       = statsByVendor[vendor]['email']
        setDays     = statsByVendor[vendor]['setDays']
        costPerSet  = statsByVendor[vendor]['costPerSet']
        vendorCost  = statsByVendor[vendor]['subtotal']
        isTaxExempt = statsByVendor[vendor]['isTaxExempt']
        tax         = statsByVendor[vendor]['tax']
        total       = statsByVendor[vendor]['total']

        summary.append([
            vendor,
            email,
            setDays,
            '${:,.2f}'.format(costPerSet),
            '${:,.2f}'.format(vendorCost),
            isTaxExempt,
            '${:,.2f}'.format(tax),'${:,.2f}'.format(total)
            ])

    CreateResultsCSV('Billing Summary',summary)
    return summary

def GetVendorAcronym(vendor):
    acronym = ""
    
    for word in vendor.split():
        acronym += word[0]
    
    acronym += str(len(vendor))

    return acronym


def GetInvoiceNumber(vendor, start):
    part0 = start.strftime("%y")
    part1 = "-"
    part2 = start.strftime("%m")
    part3 = "-"
    part4 = GetVendorAcronym(vendor)

    return part0 + part1 + part2 + part3 + part4

def GenerateInvoices(ordersByVendor, statsByVendor, start):
    os.mkdir("/Users/workhorse/Downloads/Invoices")

    for vendor in ordersByVendor:
        invoiceNumber = GetInvoiceNumber(vendor, start)

        invoice = FPDF('P',"pt",'Letter')
        invoice.add_page()
        invoice.set_font("helvetica",size=10)

        invoice.image("/Users/workhorse/Scripts/SWBSA/SWBSA.png",80,30,209.05,150)
        
        invoice.cell(550,12,"INVOICE",new_x="LMARGIN", new_y="NEXT",align="R")

        invoice.set_font("helvetica",style="B",size=8)
        invoice.cell(40,12,"",new_x="LMARGIN", new_y="NEXT",align="L")

        invoice.cell(40,12,"",new_x="LMARGIN", new_y="NEXT",align="L")

        invoice.cell(360,12,"BILL TO:",align="R")
        invoice.cell(40,12,vendor,new_x="LMARGIN", new_y="NEXT",align="L")

        invoice.cell(360,12,"EMAIL:",align="R")
        invoice.cell(40,12,statsByVendor[vendor]['email'],new_x="LMARGIN", new_y="NEXT",align="L")

        invoice.cell(360,12,"INVOICE #:",align="R")
        invoice.cell(40,12,invoiceNumber,new_x="LMARGIN", new_y="NEXT",align="L")

        invoice.cell(305,12,"")
        invoice.set_fill_color(234, 153, 153) # RED
        invoice.cell(250,12,"SOUTH WALTON BEACH SERVICE ASSOCIATION",new_x="LMARGIN", new_y="NEXT",align="C",fill=True)

        invoice.cell(305,12,"")
        invoice.set_fill_color(252, 229, 205) # ORANGE
        invoice.set_font("helvetica",size=8)
        invoice.cell(110,12,"VENDOR SET DAYS:",align="R",fill=True)
        invoice.cell(140,12,'{:,.0f}'.format(statsByVendor[vendor]['setDays']),new_x="LMARGIN", new_y="NEXT",align="R",fill=True)

        invoice.cell(305,12,"")
        invoice.set_fill_color(255, 242, 204) # YELLOW
        invoice.cell(110,12,"COST PER SET:",align="R",fill=True)
        invoice.cell(140,12,'${:,.2f}'.format(statsByVendor[vendor]['costPerSet']),new_x="LMARGIN", new_y="NEXT",align="R",fill=True)

        invoice.cell(305,12,"")
        invoice.set_fill_color(217, 234, 211) # GREEN
        invoice.cell(110,12,"SUBTOTAL:",align="R",fill=True)
        invoice.cell(140,12,'${:,.2f}'.format(statsByVendor[vendor]['subtotal']),new_x="LMARGIN", new_y="NEXT",align="R",fill=True)

        invoice.cell(305,12,"")
        invoice.set_fill_color(207, 226, 243) # BLUE
        invoice.cell(110,12,"TAX:",align="R",fill=True)
        invoice.cell(140,12,'${:,.2f}'.format(statsByVendor[vendor]['tax']),new_x="LMARGIN", new_y="NEXT",align="R",fill=True)

        invoice.cell(305,12,"")
        invoice.set_fill_color(217, 210, 233) # PURPLE
        invoice.set_font("helvetica",style="B",size=8)
        invoice.cell(110,12,"TOTAL:",align="R",fill=True)
        invoice.cell(140,12,'${:,.2f}'.format(statsByVendor[vendor]['total']),new_x="LMARGIN", new_y="NEXT",align="R",fill=True)
        
        invoice.set_fill_color(239, 239, 239) # GRAY
        invoice.cell(152.5,12,"Please remit check payment to:",align="L",fill=True)
        invoice.set_font("helvetica",size=18)
        invoice.cell(152.5,36,'${:,.2f}'.format(statsByVendor[vendor]['total']),align="C")
        invoice.set_font("helvetica",style="B",size=8)
        invoice.cell(250,16,"Please call Phillip Poundstone",align="C",fill=True)
        invoice.cell(1,12,"",new_x="LMARGIN", new_y="NEXT",align="C")

        invoice.set_font("helvetica",size=8)
        invoice.cell(152.5,12,"South Walton Beach Service Association",align="L",fill=True)
        invoice.cell(152.5,12,"")
        invoice.set_font("helvetica",style="B",size=8)
        invoice.cell(250,16,"with billing questions:",align="C",fill=True)
        invoice.cell(1,12,"",new_x="LMARGIN", new_y="NEXT",align="C")

        invoice.set_font("helvetica",size=8)
        invoice.cell(152.5,12,"605 North County Highway 393, Unit 13A",align="L",fill=True)
        invoice.cell(152.5,12,"")
        invoice.set_font("helvetica",style="B",size=8)
        invoice.cell(250,24,"850-832-8715",align="C",fill=True)
        invoice.cell(1,12,"",new_x="LMARGIN", new_y="NEXT",align="C")
        
        invoice.set_font("helvetica",size=8)
        invoice.cell(152.5,12,"Santa Rosa Beach, FL 32459",align="L",fill=True)
        invoice.set_fill_color(0, 0, 0) # BLACK
        invoice.set_text_color(255,255,255) # WHITE
        invoice.set_font("helvetica",style="B",size=6)
        invoice.cell(152.5,12,"INCLUDES SET / DAY FEE TO WALTON COUNTY",align="C",fill=True)
        invoice.set_fill_color(239, 239, 239) # GRAY
        invoice.set_text_color(0,0,0) # BLACK
        invoice.set_font("helvetica",size=8)
        invoice.cell(250,12,"",new_x="LMARGIN", new_y="NEXT")

        invoice.cell(250,12,"",new_x="LMARGIN", new_y="NEXT")

        invoice.set_fill_color(239, 239, 239) # GRAY
        invoice.set_font("helvetica",style="B",size=8)
        invoice.cell(68.98, 12,"SWBSA ID",align="C",fill=True,border=True)
        invoice.cell(86.49, 12,"BEACH ACCESS",align="C",fill=True,border=True)
        invoice.cell(102.93,12,"ORDER NAME",align="C",fill=True,border=True)
        invoice.cell(73.75,12,"ORDER NUMBER",align="C",fill=True,border=True)
        invoice.cell(49.35,12,"START",align="C",fill=True,border=True)
        invoice.cell(47.75,12,"END",align="C",fill=True,border=True)
        invoice.cell(32.37,12,"SETS",align="C",fill=True,border=True)
        invoice.cell(31.84,12,"DAYS",align="C",fill=True,border=True)
        invoice.cell(61.55,12,"SET DAYS",new_x="LMARGIN", new_y="NEXT",align="C",fill=True,border=True)

        invoice.set_fill_color(255, 255, 255) # WHITE
        invoice.set_font("helvetica",size=8)

        for order in ordersByVendor[vendor]:
            invoice.cell(68.98, 12,order[1],align="L",fill=True,border=True)
            invoice.cell(86.49, 12,order[2],align="L",fill=True,border=True)
            invoice.cell(102.93,12,order[0],align="L",fill=True,border=True)
            invoice.cell(73.75,12,order[6],align="L",fill=True,border=True)
            invoice.cell(49.35,12,order[10],align="L",fill=True,border=True)
            invoice.cell(47.75,12,order[11],align="L",fill=True,border=True)
            invoice.cell(32.37,12,str(order[4]),align="L",fill=True,border=True)
            invoice.cell(31.84,12,str(order[12]),align="L",fill=True,border=True)
            invoice.cell(61.55,12,str(order[13]),new_x="LMARGIN", new_y="NEXT",align="L",fill=True,border=True)

        invoice.output("/Users/workhorse/Downloads/Invoices/"+vendor+".pdf")

def GenerateVendorCSVs(ordersByVendor):
    os.mkdir('/Users/workhorse/Downloads/CSVs')

    for vendor in ordersByVendor:
        with open("/Users/workhorse/Downloads/CSVs/"+vendor.replace('/','')+".csv", 'w') as file:
            write = csv.writer(file)
            write.writerows(ordersByVendor[vendor])

def GenerateMVPReport(accessUtilization, vendorUtilization, summary, start, end):
    report = []

    for row in accessUtilization:
        report.append(row)
    
    report.append([])
    
    for index, row in enumerate(report):
        report[index].append('')
    
    report[0].append("DATES REPORTING ON:")
    report[0].append(str(start))
    report[0].append(str(end))
    
    report[2].append("VENDOR MONTHLY PERCENTAGES")
    for index, row in enumerate(vendorUtilization):
        for cell in row:
            report[index + 3].append(cell)
    
    report[4 + len(vendorUtilization)].append("SUMMARY OF TOTALS")
    for index, row in enumerate(summary):
        if len(report[index + 5 + len(vendorUtilization)]) != 6:
            for i in range(5): report[index + 5 + len(vendorUtilization)].append('')

        for cell in row:
            report[index + 5 + len(vendorUtilization)].append(cell)
    
    CreateResultsCSV('MVP Report', report)

def RemoveReportingFiles():
    path = "/Users/workhorse/Downloads/"
    os.chdir(path)
    os.remove('Export_ExportRentalsByDay.csv')
    os.remove('Export_Walkups.csv')
    os.remove('SWBSA Billing Master - ACCESSES.csv')
    os.remove('SWBSA Billing Master - CONFIG.csv')
    os.remove('SWBSA Billing Master - MEMBERS.csv')
    os.remove('SWBSA Billing Master - ONE-OFF ADDS.csv')
    return


start = sys.argv[1]
end   = sys.argv[2]

GetCSVFromGoogleSheetTab(credentials.GoogleSheetIDs["SWBSA Billing Master"],"554242907") # SWBSA Billing Master - CONFIG.csv
GetCSVFromGoogleSheetTab(credentials.GoogleSheetIDs["SWBSA Billing Master"],"497664029") # SWBSA Billing Master - MEMBERS.csv
GetCSVFromGoogleSheetTab(credentials.GoogleSheetIDs["SWBSA Billing Master"],"691606791") # SWBSA Billing Master - ACCESSES.csv
GetCSVFromGoogleSheetTab(credentials.GoogleSheetIDs["SWBSA Billing Master"],"15994011")  # SWBSA Billing Master - ONE-OFF ADDS.csv
RunScript('GetSubmissionsSWBSA')                                                         # Export_ExportRentalsByDay.csv
RunScriptWithArguments('GetWalkupsSWBSA', [start, end])                                  # Export_Walkups.csv

start = datetime.strptime(sys.argv[1],"%m/%d/%Y")
end   = datetime.strptime(sys.argv[2],"%m/%d/%Y")

orders   = []
walkups  = []
config   = []
members  = []
accesses = []

orders   = GetOrderDataFromCSV()
walkups  = GetWalkupDataFromCSV()
config   = GetConfigDataFromCSV()
members  = GetMemberDataFromCSV()
accesses = GetAccessDataFromCSV()

while orders == [] and walkups == [] and config == [] and members == [] and accesses == []: continue

results = GetRelevantOrdersByRange(start, end, orders)

setDayCount    = results[0]
ordersByVendor = results[1]
ordersByAccess = results[2]

statsByVendor  = GetStatsByVendor(ordersByVendor, members, config['CostPerSet'], config['TaxRate'])

# Code Enforcement Reports
accessUtilization = GenerateAccessUtilization(accesses, ordersByAccess, walkups, int(config['CountyFee']), start)
vendorUtilization = GenerateVendorUtilization(statsByVendor, setDayCount, start)
summary           = GenerateSummary(setDayCount, walkups, int(config['CountyFee']))

CreateResultsCSV("accesses", accessUtilization)
CreateResultsCSV("vendors", vendorUtilization)
CreateResultsCSV("summary",summary)

GenerateMVPReport(accessUtilization, vendorUtilization, summary, sys.argv[1], sys.argv[2])

# SWBSA Reports
GenerateBillingSummary(statsByVendor)
# GenerateInvoices(ordersByVendor, statsByVendor, start)
GenerateVendorCSVs(ordersByVendor)

RemoveReportingFiles()