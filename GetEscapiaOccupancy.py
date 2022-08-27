from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path

import credentials
import webbrowser
import time
import csv
import sys
import os


pullType = sys.argv[1] # all, arrival, departure
start    = sys.argv[2] # start date: MM/dd/YYYY
end      = sys.argv[3] # end date: MM/dd/YYY

options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)

def SignInToEscapia():
    driver.get("http://" + credentials.Escapia["partners"][0][0] + ".escapia.com")

    username = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.ID,"UserName")))
    username.clear()
    username.send_keys(credentials.Escapia["partners"][0][1])

    password = driver.find_element(By.ID, "Password")
    password.clear()
    password.send_keys(credentials.Escapia["partners"][0][2])

    button = driver.find_element(By.ID,"btnLogin")
    button.click()


def GetPullType(pullType):
    match pullType.lower():
        case 'all':
            return 0
        case 'arrival':
            return 1
        case 'arrive':
            return 1
        case 'departure':
            return 2
        case 'depart':
            return 2
        case _:
            return 0


def NavigateToWebsite():
    driver.get(credentials.integraRental_SWBSA["url"])


def ReformatDate(date):
    return date.replace('/',"%2F")


def GetEscapiaURL(partner, pullType, start, end):
    part0 = "https://reports.escapia.com/ReportServer/Pages/ReportViewer.aspx?%2FEscapiaReports%2FHousekeeping%2FHousekeeping%20Arrival%20Departure%20Report%20-%20Excel%201%20line&Hostname="
    part1 = partner
    part2 = ".escapia.com&StartDate="
    part3 = start
    part4 = "%2000%3A00%3A00&EndDate="
    part5 = end
    part6 = "%2000%3A00%3A00&Housekeeper=0&Select="
    part7 = str(pullType)
    part8 = "&BookingStatus=255&SortBy=0&Location=0&Office=0&rs%3AParameterLanguage=&rs%3ACommand=Render&rs%3AFormat=CSV"
    return part0 + part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8

def WaitForDownload():
    time.sleep(3)

def GetFileName(pullType, partnerName):
    prefix = ""

    match pullType:
        case 0:
            prefix = "all_"
        case 1:
            prefix = "a_"
        case 2:
            prefix = "d_"
        case _:
            prefix = "all_"
    
    filename = str(Path.home() / "Downloads")
    filename += prefix + partnerName + ".csv"

    return filename


def ChangeFileNames(pullType, partners):
    print("renaming files...")

    WaitForDownload()
    pullType = GetPullType(pullType)
    path     = str(Path.home() / "Downloads")

    match len(partners):
        case 0:
            return
        case 1:
            filename = GetFileName(pullType, partners[0][0])
            os.rename(path + "Housekeeping Arrival Departure Report - Excel 1 line.csv", filename)
        case _:
            filename = GetFileName(pullType, partners[0][0])
            os.rename(path + "Housekeeping Arrival Departure Report - Excel 1 line.csv", filename)
            
            for index, partner in enumerate(partners[1:]):
                filename = GetFileName(pullType, partner[0])
                original = path + "Housekeeping Arrival Departure Report - Excel 1 line (" + str(index+1) + ").csv"

                os.rename(original, filename)


def CombineReports():
    print("combining reports...")

    path = str(Path.home() / "Downloads")
    os.chdir(path)

    data = []

    with open("Housekeeping Arrival Departure Report - Excel 1 line.csv") as file:
        reader = list(csv.reader(file))

        for row in reader[:-1]:
            data.append(row)
    
    os.remove("Housekeeping Arrival Departure Report - Excel 1 line.csv")

    for file in os.listdir(path):
        if "Housekeeping Arrival Departure Report - Excel 1 line (" in file:
            with open(file) as report:
                reader = list(csv.reader(report))

                for row in reader[1:-1]:
                    data.append(row)

            os.remove(file)
    
    with open("a_escapia.csv", 'w') as file:
        write = csv.writer(file)
        write.writerows(data)


def FetchEscapiaOccupancy(pullType, start, end):
    pullType = GetPullType(pullType)
    start    = ReformatDate(start)
    end      = ReformatDate(end)

    driver.get(GetEscapiaURL(credentials.Escapia["partners"][0][0], pullType, start, end))
    # Login(credentials.Escapia["partners"][0])
    print("grabbing",credentials.Escapia["partners"][0][0],"occupancy...")
    WaitForDownload()

    for partner in credentials.Escapia["partners"][1:]:
        print("grabbing",partner[0],"occupancy...")
        driver.get(GetEscapiaURL(partner[0], pullType, start, end))
        WaitForDownload()


print("navigating to login page...")

SignInToEscapia()
FetchEscapiaOccupancy(pullType, start, end)
CombineReports()

print("done")
driver.quit()
webbrowser.open("file://" + str(Path.home() / "Downloads"))