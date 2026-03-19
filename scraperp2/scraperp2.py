import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
url = driver.get("https://www.ycombinator.com/companies?batch=Spring%202026&batch=Winter%202026&batch=Fall%202025")

while True:
    count = len(driver.find_elements(By.CLASS_NAME, "_coName_18olp_472"))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    if count == len(driver.find_elements(By.CLASS_NAME, "_coName_18olp_472")):
        break


company_names =[]
company_description = []

data = driver.page_source

soup = BeautifulSoup(data,'html.parser',from_encoding='utf-8')
company_names_div = soup.find_all('div',class_='my-0 py-0')
for i in company_names_div:
    company_names.append(i.find_all('span',class_='_coName_18olp_472'))
company_description_div = soup.find_all('div',class_='mb-1.5 text.sm')
for i in company_description_div:
    company_description.append(i.find_all('span'))
companies = list(zip(company_names,company_description))

print(soup)

with open('yccompanies','w') as new:
    json.dump(companies,new)