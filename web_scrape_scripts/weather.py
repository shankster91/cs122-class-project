'''
Pull weather info by zip
'''

import bs4
import csv
import re
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options

def start_driver(headless=True):
    
    ff_options = Options()
    if headless:
        ff_options.add_argument('--headless')
    driver = webdriver.Firefox(options=ff_options, executable_path="./geckodriver")
    driver.set_page_load_timeout(10)
    driver.get("https://www.weatherbase.com/")

    return driver

def get_weather_by_zip(zip_code, driver=None, headless=True):

    if driver == None:
        driver = start_driver(headless)
    #time.sleep(1)

    searchbox = driver.find_element_by_id("query")
    searchbox.click()
    #time.sleep(1)
    searchbox.clear()
    #time.sleep(1)
    searchbox.send_keys(zip_code)
    #time.sleep(1)
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/table/tbody/tr[2]/td[4]/form/button")))
    #driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/table/tbody/tr[2]/td[4]/form/button").click()
    try:
        button.click()
    except TimeoutException:
        searchbox = driver.find_element_by_id("query")
        searchbox.click()
        searchbox.clear()
        searchbox.send_keys(zip_code)
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/table/tbody/tr[2]/td[4]/form/button")))
        try:
            button.click()
        except TimeoutException:
            searchbox = driver.find_element_by_id("query")
            searchbox.click()
            searchbox.clear()
            searchbox.send_keys(zip_code)
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/table/tbody/tr[2]/td[4]/form/button"))) 
            button.click() 

    #time.sleep(1)
    page_source = driver.page_source

    soup = bs4.BeautifulSoup(page_source, "html5lib")
    link = soup.find("a", attrs = {"class": "redglow"})

    try:
        new_url = "https://www.weatherbase.com" + link['href']
        driver.get(new_url)
        #time.sleep(1)

        fin_page_source = driver.page_source
        soup = bs4.BeautifulSoup(fin_page_source, "html5lib")
        tables = soup.find_all("table", attrs = {"class": "weather-table"})

        temp = -1
        precip = -1
        for table in tables:
            if table.find("div").text == 'Average Temperature':
                data_table = table.find_next("table")
                temp = data_table.find("td", attrs = {"class": "data"}).text
                #print("Average Temperature:", temp)
            elif table.find("div").text == 'Average Precipitation':
                data_table = table.find_next("table")
                precip = data_table.find("td", attrs = {"class": "data"}).text
                #print("Average Precipitation:", precip)
    except TimeoutException:
        temp = -1
        precip = -1
    except:
        temp = -1
        precip = -1

    #print("Done with zip:", zip_code)
    return (temp, precip)

def get_weather_lst(zip_list, headless=True):

    driver = start_driver(headless)

    temp_lst = []
    precip_lst = []
    index = 0
    for zip_code in zip_list:
        temp, precip = get_weather_by_zip(zip_code, driver, headless)
        temp_lst.append(temp)
        precip_lst.append(precip)
        index += 1
    
        if index % 100 == 0:
            time.sleep(1)
            #print("Done with zip #", index)

    driver.close()
    
    return temp_lst, precip_lst

def weather_to_csv(zip_list, filename, headless=True):

    temp_lst, precip_lst = get_weather_lst(zip_list, headless)
    pd_dict = {'zip': zip_list, 'temperature': temp_lst, 'precipitation': precip_lst}
    df = pd.DataFrame(pd_dict)

    #df.to_csv(filename, index = False)
    df.to_csv(filename, index = False, mode = 'a', header = False)

def batch_runner(zip_list, filename, headless=True):

    index = 0
    while index < len(zip_list):
        batch = zip_list[index:index + 100]
        weather_to_csv(batch, filename, headless)
        index += 100
        print("Batch done, index=", index)



#delay = 10 # seconds
#try:
#    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'cell320left')))
#    print("Page is ready!")
#except TimeoutException:
#    print("Loading took too much time!")

#html = driver.page_source
#time.sleep(2)
#with open("test.txt", 'w') as sys.stdout:
#    print(html)

# def get_weather_by_zip(zip_code):
#     url = "https://www.weatherbase.com/search/search.php3?query=30324"
#     req = util.get_request(url)
#     if req:
#         #text = util.read_request(req)
#         text = req.text
#     else:
#         score =  -1
#         text = None
#     if text:
#         soup = bs4.BeautifulSoup(text, "html5lib")
#         divs = soup.find_all('div', attrs = {'id': 'cell320left'})
    
#     return text