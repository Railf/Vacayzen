from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from pathlib import Path

import pandas as pd
import time


options = webdriver.ChromeOptions()
driver  = webdriver.Chrome(options=options)

driver.get("https://www.vacasa.com/search?place=/usa/TOPSL-Beach-Racquet-Resort/")

units = []

for i in range(1,10,1):
    print("gathering units from page",i)

    for j in range(1,25,1):
        xml = "//*[@id='search-results']/div[3]/div[" + str(j) + "]/div/div/div[1]/h2/a"
        unit = driver.find_element(By.XPATH,xml).text

        page = driver.find_element(By.XPATH,"/html/body/div[4]/div[2]/div[1]/div[5]/div[1]").text
        units.append(unit)
        
    driver.find_element(By.XPATH,"//button[text()='next']").click()
    time.sleep(1)

xml = "//*[@id='search-results']/div[3]/div[1]/div/div/div[1]/h2/a"
unit = driver.find_element(By.XPATH,xml).text
units.append(unit)

for unit in units:
    print(unit)

print(len(units))

driver.quit()