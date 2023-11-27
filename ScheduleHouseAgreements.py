from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path

import pandas as pd

import credentials
import time


options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)
wait    = WebDriverWait(driver, 30)

agreements = []


def NavigateToWebsite():
    print("navigating to login page...")
    driver.get(credentials.integraRental["url"])


def Login(username, password):
    print("logging in...")
    email    = wait.until(EC.presence_of_element_located((By.ID,"txtEmail"))).send_keys(username)
    passcode = driver.find_element(By.ID,"txtpassword").send_keys(password)
    login    = driver.find_element(By.ID,"btnlogin").click()
    validate = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div[2]/div/div[3]/button[2]"))).click()

def NavigateToNewReservation():
    print("navigating to new reservation page...")
    time.sleep(0.5)
    driver.get(credentials.integraRental["url-NewReservation"])


def NavigateToOrder(order):
    print("navigating to rental agreement: " + str(order) + " ...")
    search = wait.until(EC.presence_of_element_located((By.ID,"txtSearchBox"))).send_keys(order)
    button = driver.find_element(By.ID,"btn_Search_AG_ById").click()
    time.sleep(5)


def ScheduleAssetsOnDateForCustomer(asset, quantity, date, customer):
    date = pd.to_datetime(date)
    date = date.strftime("%m/%d/%Y")
    date = date + " 10:00 AM"

    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    
    field = wait.until(EC.presence_of_element_located((By.ID,"txtAsset"))).send_keys(asset)
    field = wait.until(EC.presence_of_element_located((By.ID,"txtBeginDate")))
    field.clear()
    field.send_keys(date)
    time.sleep(0.75)
    field = wait.until(EC.element_to_be_clickable((By.ID,"chkInfinite"))).click()
    time.sleep(0.75)
    field = wait.until(EC.element_to_be_clickable((By.ID,"btnSearchAsset"))).click()
    time.sleep(1.5)
    field = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div[4]/div/div[2]/div[3]/div[3]/div/div/div/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]"))).click()
    time.sleep(1)
    field = wait.until(EC.presence_of_element_located((By.ID,"txtcust"))).send_keys(customer)
    field = wait.until(EC.element_to_be_clickable((By.ID,"btncust"))).click()
    time.sleep(2)
    field = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[29]/div[2]/div[2]/div/div/div[1]/table/tbody/tr/td[1]"))).click()
    time.sleep(1)
    field = wait.until(EC.presence_of_element_located((By.ID,"txtCustomerName"))).clear()
    field = wait.until(EC.presence_of_element_located((By.ID,"txtCustomerName"))).send_keys(customer)
    time.sleep(0.75)
    field = wait.until(EC.element_to_be_clickable((By.ID,"btnContinue"))).click()
    time.sleep(2)
    field = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[28]/div[2]/div[4]/div/div/div/div[1]/div/table/tbody/tr/td/div/div/ol/li/div[2]/table/tbody/tr[2]/td[7]/span/span/input[2]"))).send_keys(quantity)
    time.sleep(0.75)
    field = wait.until(EC.element_to_be_clickable((By.ID,"btnAddtoReservation1"))).click()
    time.sleep(2)
    field = wait.until(EC.presence_of_element_located((By.ID,"MainContent_lblAgreementNo")))
    
    print("rental agreement created:", field.text)
    return field.text


def AssignShipTo(shipto):
    field = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/form/div[4]/div/div[2]/div[3]/div[1]/div[1]/div[2]/div[5]/div/div/ul/li[2]"))).click()
    field = wait.until(EC.element_to_be_clickable((By.ID,"spShipToSearchRemove"))).click()
    time.sleep(0.75)
    field = wait.until(EC.presence_of_element_located((By.ID,"txtShipTo"))).send_keys(shipto)
    field = wait.until(EC.element_to_be_clickable((By.ID,"btnShipToContact"))).click()
    time.sleep(1)
    field = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[116]/div[2]/div[2]/div/div/div[1]/table/tbody/tr/td[1]"))).click()
    time.sleep(2)
    field = wait.until(EC.element_to_be_clickable((By.ID,"MainContent_btnsave1"))).click()
    time.sleep(5)



data         = pd.read_csv('/Users/workhorse/Downloads/agreements.csv')
data.columns = ['customer','unit','asset','quantity','date','shipto']

try:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])
except:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])

for index, row in data.iterrows():
    NavigateToNewReservation()

    print("creating rental agreement for", row.unit, "... ", end="")

    agreement = ScheduleAssetsOnDateForCustomer(row.asset, row.quantity, row.date, row.customer)
    AssignShipTo(row.shipto)
    
    agreements.append([row.customer, row.unit, agreement])

df = pd.DataFrame(agreements, columns=['customer','unit','rental agreement'])
df.to_csv('/Users/workhorse/Downloads/results.csv', index=False)

print("done")
driver.quit()