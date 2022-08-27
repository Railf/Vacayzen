from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
from pathlib import Path
from glob import glob

import credentials
import time
import os


options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)
wait    = WebDriverWait(driver, 100)

def NavigateToWebsite():
    print("navigating to login page...")
    driver.get(credentials.integraRental_SWBSA["url"])

def Login(username, password):
    print("logging in...")
    email    = wait.until(EC.presence_of_element_located((By.ID,"txtEmail"))).send_keys(username)
    passcode = driver.find_element(By.ID,"txtpassword").send_keys(password)
    login    = driver.find_element(By.ID,"btnlogin").click()
    print("navigating to report...")

def GetPullStartDate():
    return ("01/01/" + date.today().strftime("%Y"))

def GetPullEndDate():
    return ("12/31/" + date.today().strftime("%Y"))

def PullReport():
    print("requesting the report...")
    start = GetPullStartDate()
    end   = GetPullEndDate()

    startDate = wait.until(EC.presence_of_element_located((By.ID,"MainContent_startDate")))
    startDate.clear()
    startDate.send_keys(start)

    endDate   = driver.find_element(By.ID, "MainContent_endDate")
    endDate.clear()
    endDate.send_keys(end)

    search = driver.find_element(By.ID, "btnSearch").click()
    time.sleep(1)
    result = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='relatedProductGrid']/div[2]/table/tbody/tr[1]/td[1]")))
    export = driver.find_element(By.ID, "ExportCsv").click()

    WaitForDownload("Export_ExportRentalsByDay","csv")

def WaitForDownload(filename, extension):
    print("downloading...")

    os.chdir(str(Path.home() / "Downloads"))

    while not glob(filename + "*." + extension):
        continue


NavigateToWebsite()
Login(credentials.integraRental_SWBSA["username"],credentials.integraRental_SWBSA["password"])
PullReport()

print("done")
driver.quit()