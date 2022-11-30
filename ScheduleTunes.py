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


def NavigateToAgreement(agreement):
    print("navigating to rental agreement: " + str(agreement) + " ...")
    search = wait.until(EC.presence_of_element_located((By.ID,"txtSearchBox"))).send_keys(agreement)
    button = driver.find_element(By.ID,"btn_Search_AG_ById").click()
    time.sleep(5)


def ScheduleTune(date):
    date = pd.to_datetime(date)
    date = date.strftime("%m/%d/%Y")
    date = date + " 9:00 AM"

    try:
        if EC.presence_of_element_located((By.ID,"btnmodalClose")): driver.find_element(By.ID,"btnmodalClose").click()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        wait.until(EC.presence_of_element_located((By.ID,"MainContent_btnAddServiceItem"))).click()
    except:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        wait.until(EC.presence_of_element_located((By.ID,"MainContent_btnAddServiceItem"))).click()
    
    time.sleep(0.5)
    service = wait.until(EC.presence_of_element_located((By.ID,"serviceAutocomplete"))).send_keys('EOY Tune')
    time.sleep(0.5)
    service = wait.until(EC.element_to_be_clickable((By.ID,"serviceAutocomplete_listbox"))).click()
    service = driver.find_element(By.ID,"ServiceReturnDate").send_keys(date)

    button = driver.find_element(By.ID,"btnAddServiceReservation").click()
    time.sleep(3)



data = pd.read_csv('/Users/workhorse/Downloads/tunes.csv')
data = data[['Service Date','INT #']]
data.columns = ['date','agreement']

try:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])
except:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])

for index, row in data.iterrows():
    NavigateToAgreement(row.agreement)
    ScheduleTune(row.date)


print("done")
driver.quit()