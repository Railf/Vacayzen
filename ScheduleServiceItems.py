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
    time.sleep(1)
    email    = wait.until(EC.presence_of_element_located((By.ID,"txtEmail"))).send_keys(username)
    passcode = driver.find_element(By.ID,"txtpassword").send_keys(password)
    login    = driver.find_element(By.ID,"btnlogin").click()
    try:
        print("validating...")
        validate = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div/div[2]/div/div[3]/button[2]"))).click()
    except:
        print("validation not needed")


def NavigateToOrder(order):
    print("navigating to rental agreement: " + str(order) + " ...")
    search = wait.until(EC.presence_of_element_located((By.ID,"txtSearchBox"))).send_keys(order)
    button = driver.find_element(By.ID,"btn_Search_AG_ById").click()
    time.sleep(5)


def ScheduleServiceOnDateWithNote(service, date, note):
    date = pd.to_datetime(date)
    date = date.strftime("%m/%d/%Y")
    date = date + " 9:00 AM"

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    try:
        if EC.presence_of_element_located((By.XPATH,"/html/body/div[117]/div[2]/div[2]/div/button")): driver.find_element(By.XPATH,"/html/body/div[117]/div[2]/div[2]/div/button").click()
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)
        wait.until(EC.presence_of_element_located((By.ID,"MainContent_btnAddServiceItem"))).click()
    except:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.5)
        wait.until(EC.presence_of_element_located((By.ID,"MainContent_btnAddServiceItem"))).click()
    
    service = wait.until(EC.presence_of_element_located((By.ID,"serviceAutocomplete"))).send_keys(service)
    time.sleep(0.75)

    service = wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='serviceAutocomplete_listbox']/li"))).click()
    time.sleep(0.75)

    if not pd.isna(note):
        service = driver.find_element(By.ID,"textAreaLineNote").send_keys(note)
        time.sleep(0.75)
    
    service = driver.find_element(By.ID,"ServiceReturnDate").send_keys(date)
    time.sleep(0.75)

    button = driver.find_element(By.ID,"btnAddServiceReservation").click()
    time.sleep(3)



data         = pd.read_csv('/Users/ralphmccracken/Downloads/services.csv')
data.columns = ['service','note','date','order']

try:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])
except:
    NavigateToWebsite()
    Login(credentials.integraRental["username"],credentials.integraRental["password"])

for index, row in data.iterrows():
    NavigateToOrder(row.order)
    ScheduleServiceOnDateWithNote(row.service, row.date, row.note)

print("done")
driver.quit()