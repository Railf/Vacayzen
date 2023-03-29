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
    print("grabbing data from BEACHY REPORT.csv...")

    data = []
    with open(str(Path.home() / "Downloads/BEACHY REPORT.csv")) as file:
        reader = csv.reader(file)

        for row in reader:
            data.append(row)
    
    return data

def NavigateToNewOrderScreen():
    driver.get(credentials.beachy_Vacayzen["url"])

def ProvideTextToID(text, id):
    driver.find_element(By.ID,id).send_keys(text)

def ProvideTextToXPATH(text, xpath):
    driver.find_element(By.XPATH, xpath).send_keys(text)

def ClickAtID(id):
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.ID, id))).click()

def ClickAtXPATH(xpath):
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

def Login():
    NavigateToNewOrderScreen()
    ProvideTextToID(credentials.beachy_Vacayzen["username"], "login_email")
    ProvideTextToID(credentials.beachy_Vacayzen["password"], "login_password")
    ClickAtID("button_sign_in")

def SubmitOrder():
    NavigateToNewOrderScreen()
    ClickAtID("select2-destination-select-container")
    ProvideTextToXPATH("Carillon Beach" + Keys.RETURN,"/html/body/span/span/span[1]/input")
    time.sleep(0.2)
    ClickAtID("select2-product-select-container")
    ProvideTextToXPATH("Seasonal Sets"  + Keys.RETURN,"/html/body/span/span/span[1]/input")


Login()
SubmitOrder()