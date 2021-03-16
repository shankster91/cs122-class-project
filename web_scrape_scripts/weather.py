'''
This file scrapes weather information by zip code from weatherbase.com.
We use Selenium as the page we need to hit uses a JS query to populate results.
We need to wait for this to occur before we can proceed.
'''

import bs4
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
    '''
    Starts Selenium webdriver
    
    Input:
    headless (bool): True if user wants to suppress browser opening
                     and have scraping happen in background
    
    Output:
    driver (Selenium webdriver)
    '''
    
    ff_options = Options()
    if headless:
        ff_options.add_argument('--headless')
    driver = webdriver.Firefox(options=ff_options, executable_path="./geckodriver")
    driver.set_page_load_timeout(10)
    driver.get("https://www.weatherbase.com/")

    return driver

def get_weather_by_zip(zip_code, driver=None, headless=True):
    '''
    Gets weather info for a single zip code

    Input:
    zip_code (str): A US zip code
    driver: Selenium webdriver
    headless (bool): Bool for whether browser window should be suppressed.

    Output:
    (temp, precip) (tuple): Avg. annual temp, precipitation for given zip code.
                            -1 represents missing values.
    '''

    if driver == None:
        driver = start_driver(headless)

    # find search box
    searchbox = driver.find_element_by_id("query")
    searchbox.click()
    searchbox.clear()
    searchbox.send_keys(zip_code)
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/table/tbody/tr[2]/td[4]/form/button")))
    # Add retry logic for when web page hangs
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

    page_source = driver.page_source

    soup = bs4.BeautifulSoup(page_source, "html5lib")
    link = soup.find("a", attrs = {"class": "redglow"})

    try:
        new_url = "https://www.weatherbase.com" + link['href']
        driver.get(new_url)

        fin_page_source = driver.page_source
        soup = bs4.BeautifulSoup(fin_page_source, "html5lib")
        tables = soup.find_all("table", attrs = {"class": "weather-table"})

        temp = -1
        precip = -1
        for table in tables:
            if table.find("div").text == 'Average Temperature':
                data_table = table.find_next("table")
                temp = data_table.find("td", attrs = {"class": "data"}).text
            elif table.find("div").text == 'Average Precipitation':
                data_table = table.find_next("table")
                precip = data_table.find("td", attrs = {"class": "data"}).text
    except TimeoutException:
        temp = -1
        precip = -1

    return (temp, precip)

def get_weather_lst(zip_list, headless=True):
    '''
    Gets weather info for a list of zip codes

    Input:
    zip_list (list): List of US zip codes
    headless (bool): Bool for whether browser window should be suppressed.

    Output:
    temp_lst (list): List of avg. annual temps for given zip codes
    precip_lst(list): List of avg. annual precipitation for given zip codes
    '''

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

    driver.close()
    
    return temp_lst, precip_lst

def weather_to_csv(zip_list, filename, headless=True):
    '''
    Gets weather info for a list of zip codes and writes to csv

    Input:
    zip_list (list): List of US zip codes
    filename (str): Filename for output
    headless (bool): Bool for whether browser window should be suppressed.

    Output:
    No return but will write out a CSV file with zips and weather info
    '''

    temp_lst, precip_lst = get_weather_lst(zip_list, headless)
    pd_dict = {'zip': zip_list, 'temperature': temp_lst, 'precipitation': precip_lst}
    df = pd.DataFrame(pd_dict)

    #df.to_csv(filename, index = False)
    df.to_csv(filename, index = False, mode = 'a', header = False)

def batch_runner(zip_list, filename, headless=True):
    '''
    Runs code in batches of zips and returns info on progress.
    This way if there is an error at some point we don't lose
    everything.

    Input:
    zip_list (list): List of US zip codes
    filename (str): Filename for output
    headless (bool): Bool for whether browser window should be suppressed.

    Output:
    No return but will write out a CSV file with zips and weather info,
    in batches of 100 zips
    '''

    index = 0
    while index < len(zip_list):
        batch = zip_list[index:index + 100]
        weather_to_csv(batch, filename, headless)
        index += 100
        print("Batch done, index=", index)