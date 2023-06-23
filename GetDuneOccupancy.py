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
    driver.get(credentials.Dune["url"])

def Login(username, password):
    print("logging in...")
    email    = wait.until(EC.presence_of_element_located((By.ID,"user_login"))).send_keys(username)
    passcode = driver.find_element(By.ID, "user_password").send_keys(password)
    login    = driver.find_element(By.ID, "submit_button").click()
    mfa      = input("enter MFA code: ")
    mfa      = wait.until(EC.presence_of_element_located((By.ID,"ga_code"))).send_keys(mfa)
    submit   = driver.find_element(By.ID, "submit_button").click()

def NavigateToCheckoutReport():
    print("navigating to report...")
    driver.get(credentials.Dune["url-home"])
    wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div[2]/div[2]/div[4]/div/div/div/div[3]/div[2]/div/div/div[2]/div/ul/li[3]"))).click()

def PullReport():
    date = driver.find_element(By.ID, "report_end_date").click()

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
Login(credentials.Dune["username"], credentials.Dune["password"])
NavigateToCheckoutReport()
PullReport()
# PullReport()

print("done")
# driver.quit()