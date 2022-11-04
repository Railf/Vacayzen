from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path
from glob import glob

import credentials
import time
import os


options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)
wait    = WebDriverWait(driver, 30)

def NavigateToWebsite():
    print("navigating to login page...")
    driver.get(credentials.ScenicStays30A["url"])

def Login(username, password):
    print("logging in...")
    email    = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='login-form']/div[3]/input"))).send_keys(username)
    passcode = driver.find_element(By.XPATH,"//*[@id='login-form']/div[4]/input").send_keys(password)
    login    = driver.find_element(By.XPATH,"//*[@id='login-form']/div[5]/button").click()

def NavigateToReport():
    print("navigating to report...")
    tab         = wait.until(EC.presence_of_element_located((By.LINK_TEXT,"Trip Items"))).click()
    format      = Select(driver.find_element(By.XPATH,"//*[@id='spine-content']/div[11]/article/div/div/div/article[2]/div[1]/div[1]/div[2]/div[2]/label/select")).select_by_value("5d6a1c4b-a3b0-434c-be4c-b868725c6346")
    itemType    = Select(driver.find_element(By.XPATH,"//*[@id='trip-items-filters-list']/li[1]/label/select")).select_by_value("property_item")
    time.sleep(1)
    group       = Select(wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='trip-items-filters-list']/li[1]/div[2]/label[3]/select")))).select_by_value("db2eaada-35bc-47e3-a47b-4d3bad911711")
    time.sleep(1)
    orderStatus = Select(driver.find_element(By.XPATH,"//*[@id='trip-items-filters-list']/li[4]/label[1]/select")).select_by_value("booked")
    time.sleep(1)

def WaitForDownload(filename, extension):
    print("downloading...")

    os.chdir(str(Path.home() / "Downloads"))

    while not glob(filename + "*." + extension):
        continue

def PullReport():
    try:
        print("requesting report...") 
        itemStartDateFrom    = driver.find_element(By.XPATH,"//*[@id='trip-items-filters-list']/li[3]/div[1]/div/div/label[1]/span/input").click()
        itemStartDateFrom    = driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/table/thead/tr[2]/th[2]").click()
        itemStartDateFrom    = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/table/tbody/tr/td/span[1]").click()
        itemStartDateFrom    = driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/table/tbody/tr[1]/td[7]").click()

        itemStartDateTo      = driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/table/thead/tr[2]/th[2]").click()
        itemStartDateTo      = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/table/tbody/tr/td/span[12]").click()
        itemStartDateTo      = driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/table/tbody/tr[5]/td[7]").click()

        time.sleep(1)

        itemCheckoutDateFrom = driver.find_element(By.XPATH,"//*[@id='trip-items-filters-list']/li[3]/div[3]/div/div/label[1]/span/input").click()
        itemCheckoutDateFrom = driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/table/thead/tr[2]/th[2]").click()
        itemCheckoutDateFrom = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/table/tbody/tr/td/span[1]").click()
        itemCheckoutDateFrom = driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/table/tbody/tr[1]/td[7]").click()

        itemCheckoutDateTo   = driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/table/thead/tr[2]/th[2]").click()
        itemCheckoutDateTo   = driver.find_element(By.XPATH,"/html/body/div[5]/div[2]/table/tbody/tr/td/span[12]").click()
        itemCheckoutDateTo   = driver.find_element(By.XPATH,"/html/body/div[5]/div[1]/table/tbody/tr[5]/td[7]").click()
    
        time.sleep(1)

        download             = driver.find_element(By.XPATH, "//*[@id='spine-content']/div[11]/article/div/div/div/article[2]/div[1]/div[1]/div[2]/div[2]/button").click()

        WaitForDownload("trip-items","csv")

    except:
        NavigateToWebsite()
        NavigateToReport()
        print("requesting report...")
        itemStartDateFrom    = driver.find_element(By.XPATH,"//*[@id='trip-items-filters-list']/li[3]/div[1]/div/div/label[1]/span/input").click()
        itemStartDateFrom    = driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/table/thead/tr[2]/th[2]").click()
        itemStartDateFrom    = driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/table/tbody/tr/td/span[1]").click()
        itemStartDateFrom    = driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/table/tbody/tr[1]/td[7]").click()

        itemStartDateTo      = driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/table/thead/tr[2]/th[2]").click()
        itemStartDateTo      = driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/table/tbody/tr/td/span[12]").click()
        itemStartDateTo      = driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/table/tbody/tr[5]/td[7]").click()

        time.sleep(1)

        itemCheckoutDateFrom = driver.find_element(By.XPATH,"//*[@id='trip-items-filters-list']/li[3]/div[3]/div/div/label[1]/span/input").click()
        itemCheckoutDateFrom = driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/table/thead/tr[2]/th[2]").click()
        itemCheckoutDateFrom = driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/table/tbody/tr/td/span[1]").click()
        itemCheckoutDateFrom = driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/table/tbody/tr[1]/td[7]").click()

        itemCheckoutDateTo   = driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/table/thead/tr[2]/th[2]").click()
        itemCheckoutDateTo   = driver.find_element(By.XPATH,"/html/body/div[6]/div[2]/table/tbody/tr/td/span[12]").click()
        itemCheckoutDateTo   = driver.find_element(By.XPATH,"/html/body/div[6]/div[1]/table/tbody/tr[5]/td[7]").click()
    
        time.sleep(1)

        download             = driver.find_element(By.XPATH, "//*[@id='spine-content']/div[11]/article/div/div/div/article[2]/div[1]/div[1]/div[2]/div[2]/button").click()

        WaitForDownload("trip-items","csv")



NavigateToWebsite()
Login(credentials.ScenicStays30A["username"],credentials.ScenicStays30A["password"])
NavigateToReport()
PullReport()


print("done")
driver.quit()