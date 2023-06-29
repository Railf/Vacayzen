from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path

import credentials
import webbrowser
import time
import csv


options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)

def GetDataFromCSV():
    print("grabbing data from SWBSA REPORT.csv...")

    data = []
    with open(str(Path.home() / "Downloads/SWBSA REPORT.csv")) as file:
        reader = csv.reader(file)

        for row in reader:
            data.append(row)
    
    return data


def GetFormAccess(access):
    match access:
        case '395 Access':                          return '395'
        case 'Andalusia Access':                    return 'ANDALUSIA'
        case 'Azalea Access':                       return 'AZALEA'
        case 'Blue Mountain Access':                return 'BLUE MOUNTAIN'
        case 'Dune Allen Access':                   return 'DUNE ALLEN REGIONAL'
        case 'Ed Walline Access':                   return 'ED WALLINE'
        case 'Fort Panic Access':                   return 'FORT PANIC'
        case 'Gardenia Access':                     return 'GARDENIA'
        case 'Grayton Dunes Access':                return 'GRAYTON BEACH'
        case 'Gulfview Heights Access':             return 'GULFVIEW HEIGHTS'
        case 'Hickory Street Access':               return 'HICKORY'
        case 'Holly Access':                        return 'HOLLY'
        case 'Nightcap Street Access':              return 'NIGHTCAP'
        case 'One Seagrove Place Access':           return 'ONE SEAGROVE PLACE'
        case 'Orange Street Access':                return 'INLET BEACH'
        case 'Santa Clara Access':                  return 'SANTA CLARA BRAMBLE'
        case 'South Walton Lakeshore Drive Access': return 'WALTON LAKESHORE'
        case 'Spooky Lane Access':                  return 'SPOOKY LANE'
        case 'Van Ness Butler Access':              return 'VAN NESS BUTLER'
        case 'Wall Street Access':                  return 'WALL STREET'
        case 'Walton Dunes Access':                 return 'WALTON DUNES'
        case _: return access


def MapAccessToFormAccess(data):
    print("translating Vacayzen beach name to SWBSA beach name...")

    newData = []

    for row in data:
        row[0] = GetFormAccess(row[0])
        newData.append(row)
    
    return newData


def TrimTextToSize(text, size):
    return text[:size]


def ResizeTextFields(data):
    print("resizing necessary text fields to fit constraints...")

    newData = []

    for row in data:
        row[2] = TrimTextToSize(row[2],20)
        row[3] = TrimTextToSize(row[3],200)
        newData.append(row)

    return newData


def AddEmployee(data, employeeName, employeeEmail):
    print("adding employee submission data...")

    newData = []

    data[0].append("EMPLOYEE NAME")
    data[0].append("EMPLOYEE EMAIL")
    newData.append(data[0])

    for row in data[1:]:
        row.append(employeeName)
        row.append(employeeEmail)
        newData.append(row)
    
    return newData

def AddOrderStatus(data, orders):
    print("preparing results...")

    data[0].append("SUBMISSION")
    data[0].append("SUBMISSION NOTE")

    for index, row in enumerate(data[1:]):
        data[index+1].append(orders[index][0])
        data[index+1].append(orders[index][1])
    
    return data


def CreateResultsCSV(data):
    print("generating results.csv...")
    with open(str(Path.home() / "Downloads/results.csv"), 'w') as file:
        write = csv.writer(file)
        write.writerows(data)


def NagivateToForm():
    driver.get(credentials.integraRental_SWBSA["url-Form"])
    time.sleep(0.5)


def SelectBeachAccess(beachOption):
    field = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"[data-id='beach']"))).click()
    field = driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/div/div/div[4]/div/div/div/div/input")
    field.send_keys(beachOption)
    field.send_keys(Keys.ENTER)


def SelectVendor(vendorOption):
    field = driver.find_element(By.CSS_SELECTOR,"[data-id='vendor']").click()
    field = driver.find_element(By.XPATH,"/html/body/div[3]/div/div/div[2]/div/div/div[5]/div/div/div/div/input")
    field.send_keys(vendorOption)
    field.send_keys(Keys.ENTER)


def ProvideTextToID(text, id):
    driver.find_element(By.ID,id).send_keys(text)


def ClickSubmit():
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID,"btnSubmit"))).click()
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='alertModal']/div/div/div[3]/button")))


def GetSubmissionStatus():
    status = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, "//*[@id='alertModal']/div/div/div[1]/h4"))).text
    note   = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH,"//*[@id='alertModal']/div/div/div[2]/div/p"))).text
    return [status, note]


def SubmitOrder(order):
    print("submitting", order[2], "order... ", end="")

    NagivateToForm()
    SelectBeachAccess(order[0])
    SelectVendor(order[1])
    ProvideTextToID(order[2], "orderNum")
    ProvideTextToID(order[3], "orderName")
    ProvideTextToID(order[4], "startDateInput")
    ProvideTextToID(order[5], "endDateInput")
    ProvideTextToID(order[6], "numberOfSets")
    ProvideTextToID(order[7], "empName")
    ProvideTextToID(order[8], "empEmail")
    ClickSubmit()
    status = GetSubmissionStatus()

    print(status[0])
    return status


data   = GetDataFromCSV()
data   = MapAccessToFormAccess(data)
data   = ResizeTextFields(data)
data   = AddEmployee(data, "Ralph", "ralph@vacayzen.com")
orders = []

for order in data[1:]:
    order = SubmitOrder(order)
    orders.append(order)

data = AddOrderStatus(data, orders)
CreateResultsCSV(data)

print("done")
driver.quit()
webbrowser.open("file://" + str(Path.home() / "Downloads"))