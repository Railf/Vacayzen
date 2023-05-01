from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path
from glob import glob

import credentials
import time
import sys
import os

start   = sys.argv[1]
end     = sys.argv[2]

options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)
wait    = WebDriverWait(driver, 100)

def NavigateToWebsite():
    print("navigating to login page...")
    driver.get(credentials.beachy_SWBSA["url"])

def Login(username, password):
    print("logging in...")
    email    = wait.until(EC.presence_of_element_located((By.ID,"login_email"))).send_keys(username)
    passcode = driver.find_element(By.ID,"login_password").send_keys(password)
    login    = driver.find_element(By.ID,"button_sign_in").click()

def NavigateToReport():
    print("navigating to report...")
    load = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[3]/div[1]/nav/ul/li[5]/a")))
    url  = driver.current_url
    url  = url.replace("dashboard", "sandbar/admin/reports")
    driver.get(url)
    check = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div[2]/div/div[2]/input"))).click()

def PullReport(startDate, endDate):
    print("requesting the report...")

    report = Select(driver.find_element(By.ID, "report_url")).select_by_visible_text("Items Sold by Boardwalk")
    view   = driver.find_element(By.XPATH, "//*[@id='content']/div[3]/form/div/input").click()

    iframe = driver.switch_to.frame('looker-frame')
    config = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='filter-expandable-pane']/div[1]/div/span"))).click()
    dates  = Select(driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div/section/looks-subrouter/ui-view/lk-explore-dataflux/div[2]/lk-explore-content/div/div/lk-filter-pane/lk-expandable-pane/div[2]/expandable-pane-content/lk-query-filters/table/tbody/tr[1]/td[3]/lk-filter/table/tbody/tr/td[2]/select")).select_by_visible_text('is in range')
    
    start  = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div/section/looks-subrouter/ui-view/lk-explore-dataflux/div[2]/lk-explore-content/div/div/lk-filter-pane/lk-expandable-pane/div[2]/expandable-pane-content/lk-query-filters/table/tbody/tr[1]/td[3]/lk-filter/table/tbody/tr/td[2]/span[2]/span[1]/lens-explore-filter-date-picker/div/button").click()
    start  = driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div/div/div/div/div/div/input")
    start.send_keys(Keys.COMMAND,"a",Keys.BACKSPACE)
    start.send_keys(startDate)
    start.send_keys(Keys.ENTER)
    
    end    = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div/section/looks-subrouter/ui-view/lk-explore-dataflux/div[2]/lk-explore-content/div/div/lk-filter-pane/lk-expandable-pane/div[2]/expandable-pane-content/lk-query-filters/table/tbody/tr[1]/td[3]/lk-filter/table/tbody/tr/td[2]/span[3]/span/lens-explore-filter-date-picker/div/button").click()
    end    = driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div/div/div/div/div/div/input")
    end.send_keys(Keys.COMMAND,"a",Keys.BACKSPACE)
    end.send_keys(endDate)
    end.send_keys(Keys.ENTER)

    run      = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div/section/looks-subrouter/ui-view/lk-explore-dataflux/lk-explore-header/div[2]/button[1]").click()
    load     = time.sleep(5)
    options  = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div/section/looks-subrouter/ui-view/lk-explore-dataflux/lk-explore-header/div[2]/lk-explore-header-menu/lens-explore-header-menu/button").click()
    download = driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div/div/div/ul/li[1]/button").click()

    time.sleep(5)

    filename = driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div[2]/div/div/div/div[2]/div[1]/div/input")
    filename.clear()
    filename.send_keys("Export_Walkups")
    download = driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div[2]/footer/div[1]/button[1]").click()

    WaitForDownload('Export_Walkups','csv')

def WaitForDownload(filename, extension):
    print("downloading...")

    os.chdir(str(Path.home() / "Downloads"))

    while not glob(filename + "*." + extension):
        continue


NavigateToWebsite()
Login(credentials.beachy_SWBSA["username"],credentials.beachy_SWBSA["password"])
NavigateToReport()
PullReport(start, end)

print("done")
driver.quit()