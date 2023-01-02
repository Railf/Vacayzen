from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
from pathlib import Path
from glob import glob

import credentials
import time
import csv
import os


options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)
wait    = WebDriverWait(driver, 30)

def NavigateToWebsite():
    print("navigating to login page...")
    driver.get(credentials.integraRental["url"])

def Login(username, password):
    print("logging in...")
    email    = wait.until(EC.presence_of_element_located((By.ID,"txtEmail"))).send_keys(username)
    passcode = driver.find_element(By.ID,"txtpassword").send_keys(password)
    login    = driver.find_element(By.ID,"btnlogin").click()
    validate = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div[2]/div/div[3]/button[2]"))).click()

def NavigateToReport():
    print("navigating to report...")
    returns = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='sidebarmenu']/li[4]/a")))
    driver.get(credentials.integraRental["url-Returns"])

def PullReport():
    results = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='RentalDataGrid']/div[2]/table/tbody/tr[1]/td[2]")))
    export  = driver.find_element(By.XPATH,"//*[@id='validateKendoControls']/div/div/span/button[2]").click()

def WaitForDownload(filename, extension):
    print("downloading...")

    downloads = str(Path.home() / "Downloads")

    os.chdir(downloads)

    while not glob(filename + "*." + extension):
        continue

def IsOrderReturnedBeforeToday(closedDate):
    closed = datetime.strptime(closedDate,"%m/%d/%Y %I:%M %p")
    today = datetime.today()

    return (closed.date() < today.date())

def GetDataFromCSV():
    time.sleep(1)
    print("grabbing data from Export_Return.csv...")

    report = str(Path.home() / "Downloads/Export_Return.csv")

    data = []
    with open(report) as file:
        reader = csv.reader(file)

        for row in reader:
            if row[2] == 'Started - Returned All' and row[10] == row[11] and IsOrderReturnedBeforeToday(row[8]):
                data.append([row[4], row[8], row[10], row[11]])
    
    return data

def CreateCSV(name, data):
    print("generating", name + ".csv...")

    namePath = "Downloads/" + name + ".csv"

    filename = str(Path.home() / namePath)

    with open(filename, 'w') as file:
        write = csv.writer(file)
        write.writerows(data)

def CloseOrder(orderNumber):
    print("closing rental agreement #:", orderNumber + "... ", end="")
    driver.get(credentials.integraRental["url-RentalAgreement"] + orderNumber)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    close = wait.until(EC.presence_of_element_located((By.ID,"btnClose")))

    try:
        if EC.presence_of_element_located((By.ID,"btnmodalClose")): driver.find_element(By.ID,"btnmodalClose").click()
        wait.until(EC.element_to_be_clickable((By.ID,"btnClose"))).click()
    except:
        wait.until(EC.element_to_be_clickable((By.ID,"btnClose"))).click()

    time.sleep(5)
    close = wait.until(EC.element_to_be_clickable((By.ID,"btnbillingModeOK"))).click()
    time.sleep(7)

orders = []

try:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])
except:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])
    
NavigateToReport()
PullReport()
WaitForDownload("Export_Return","csv")
orders = GetDataFromCSV()

while orders == []: continue

CreateCSV("OrdersToClose", orders)

failed = []
for order in orders:
    try:
        CloseOrder(order[0])
    except:
        try:
            print("Failed. Trying again...")
            CloseOrder(order[0])
        except:
            print("Failed")
            continue
    print("Success")

print("done")
driver.quit()