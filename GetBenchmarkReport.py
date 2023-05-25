from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import date
from pathlib import Path
from glob import glob

import credentials
import os


options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)
wait    = WebDriverWait(driver, 100)

def NavigateToWebsite():
    print("navigating to login page...")
    driver.get(credentials.Benchmark["url"])

def Login(username, password):
    print("logging in...")
    email    = wait.until(EC.presence_of_element_located((By.ID,"UserName"))).send_keys(username)
    passcode = driver.find_element(By.ID, "Password").send_keys(password)
    login    = driver.find_element(By.ID, "btnLogin").click()
    answer   = wait.until(EC.presence_of_element_located((By.ID,"Answer"))).send_keys("auburn")
    login    = driver.find_element(By.ID, "btnLogin").click()

def NavigateToReport():
    print("navigating to report...")
    driver.get(credentials.Benchmark["url-Report"])

def GetPullThroughDate():
    result = date.today() + relativedelta(months=+6)
    return result.strftime("%m/%d/%Y")

def WaitForDownload(filename, extension):
    print("downloading...")

    os.chdir(str(Path.home() / "Downloads"))

    while not glob(filename + "*." + extension):
        continue

def PullReport():
    print("requesting report...")
    iframe = wait.until(EC.presence_of_element_located((By.ID,"escapia")))
    iframe = driver.switch_to.frame('escapia')

    endDate   = driver.find_element(By.NAME, "dpEndDate")
    endDate.clear()
    endDate.send_keys(GetPullThroughDate())

    excel1Line = driver.find_element(By.XPATH, "//*[@id='BookingSummaryReport']/table[1]/tbody/tr/td[3]/button[3]").click()

    WaitForDownload("output","xls")


NavigateToWebsite()
Login(credentials.Benchmark["username"], credentials.Benchmark["password"])
NavigateToReport()
PullReport()

print("done")
driver.quit()