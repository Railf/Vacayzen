from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path

import credentials
import webbrowser
import time
import csv
import os


options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)
wait    = WebDriverWait(driver, 100)

def NavigateToWebsite():
    print("navigating to login page...")
    driver.get(credentials.NRES["url"])

def Login(username, password):
    print("logging in...")
    email    = wait.until(EC.presence_of_element_located((By.ID,"P101_USERNAME"))).send_keys(username)
    passcode = driver.find_element(By.ID,"P101_PASSWORD").send_keys(password)
    login    = driver.find_element(By.ID,"P101_LOGIN").click()

def NavigateToReport():
    print("navigating to report...")
    url = driver.current_url
    url = url.replace("200:1","115:49")
    driver.get(url)

    return url

def WaitForDownload(month):
    print("downloading", month + "...")
    time.sleep(2)

def PullReport():
    print("requesting report...")

    months = {
        "january":   ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[1]", "/html/body/div[3]/div[1]/table/tbody/tr[1]/td[7]"],
        "february":  ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[2]", "/html/body/div[3]/div[1]/table/tbody/tr[1]/td[2]"],
        "march":     ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[3]", "/html/body/div[3]/div[1]/table/tbody/tr[1]/td[4]"],
        "april":     ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[4]", "/html/body/div[3]/div[1]/table/tbody/tr[1]/td[6]"],
        "may":       ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[5]", "/html/body/div[3]/div[1]/table/tbody/tr[2]/td[1]"],
        "june":      ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[6]", "/html/body/div[3]/div[1]/table/tbody/tr[1]/td[3]"],
        "july":      ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[7]", "/html/body/div[3]/div[1]/table/tbody/tr[1]/td[5]"],
        "august":    ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[7]", "/html/body/div[3]/div[1]/table/tbody/tr[5]/td[7]"],
        "september": ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[9]", "/html/body/div[3]/div[1]/table/tbody/tr[1]/td[2]"],
        "october":   ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[10]","/html/body/div[3]/div[1]/table/tbody/tr[1]/td[4]"],
        "november":  ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[10]","/html/body/div[3]/div[1]/table/tbody/tr[5]/td[7]"],
        "december":  ["/html/body/div[3]/div[2]/table/tbody/tr/td/span[12]","/html/body/div[3]/div[1]/table/tbody/tr[1]/td[1]"]
    }

    days = Select(driver.find_element(By.ID,"P49_NIGHTS")).select_by_value("30")

    resorts = driver.find_element(By.XPATH,"//*[@id='P49_RESORT_CONTAINER']/span/span[1]/span/ul/li/input")
    resorts.send_keys("Callista")
    resorts.send_keys(Keys.ENTER)
    resorts.send_keys("Emerald Coast")
    resorts.send_keys(Keys.ENTER)

    include = driver.find_element(By.XPATH,"//*[@id='P49_TYPE_CONTAINER']/span/span[1]/span/ul/li/input")
    include.send_keys("Arrivals")
    include.send_keys(Keys.ENTER)

    for month in months:
        driver.execute_script("window.scrollTo(0,0)")
        startDate = wait.until(EC.presence_of_element_located((By.ID,"P49_START"))).click()
        y         = driver.find_element(By.XPATH,"/html/body/div[3]/div[1]/table/thead/tr[1]/th[2]").click()
        m         = driver.find_element(By.XPATH,months[month][0]).click()
        d         = driver.find_element(By.XPATH,months[month][1]).click()
        search    = driver.find_element(By.ID,"P49_GO").click()
        download = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='report_544141471124269726_catch']/div[2]/a"))).click()
        WaitForDownload(month)


def CombineReports():
    print("combining reports...")

    time.sleep(2)

    path = str(Path.home() / "Downloads")
    os.chdir(path)

    data = []

    with open("Guests.csv") as file:
        reader = csv.reader(file)

        for row in reader:
            data.append(row)
    
    os.remove("Guests.csv")

    for file in os.listdir(path):
        if "Guests (" in file:
            with open(file) as report:
                reader = list(csv.reader(report))

                for row in reader[1:]:
                    data.append(row)

            os.remove(file)
    
    with open("a_360blueproperties.csv", 'w') as file:
        write = csv.writer(file)
        write.writerows(data)


NavigateToWebsite()
Login(credentials.NRES["username"],credentials.NRES["password"])
NavigateToReport()
PullReport()
CombineReports()

print("done")
driver.quit()
webbrowser.open("file://" + str(Path.home() / "Downloads"))