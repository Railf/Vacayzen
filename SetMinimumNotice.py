from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver

import pandas as pd

import credentials
import time


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


def NavigateToAsset(asset):
    time.sleep(2)
    print("navigating to asset:", str(asset), "...")
    url = credentials.integraRental["url-AssetSetup"] + str(asset)
    driver.get(url)
    time.sleep(1)
    settings = wait.until(EC.element_to_be_clickable((By.ID,"SettingTab"))).click()

def SetMinimumNotice(notice):
    print("setting notice of:", notice, "...")
    time.sleep(1)
    field = wait.until(EC.presence_of_element_located((By.ID,"txtAvaialabilityMinResNotice")))
    field.clear()
    field.send_keys(notice)
    save  = wait.until(EC.element_to_be_clickable((By.ID,"btnSettingSave"))).click()

def SetMinimumNoticeForAsset(asset, notice):
    NavigateToAsset(asset)
    SetMinimumNotice(notice)



try:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])
except:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])

df = pd.read_csv('/Users/workhorse/Downloads/AssetNotices.csv')
df.columns = ['asset','notice']
df = df.fillna("")

for index, row in df.iterrows():
    SetMinimumNoticeForAsset(row.asset, row.notice)

print("done")
driver.quit()