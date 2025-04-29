from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

debug = True

def search_denver(query):
    data_set = {}
    driver = webdriver.Chrome()
    driver.get("https://property.spatialest.com/co/denver#/")
    
    time.sleep(2)
    
    search_term = query
    
    exit_disclaimer = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/footer/div/div/div[1]/div/div/div/div[3]/button"))
    )
    exit_disclaimer.click()

    search_input = WebDriverWait(driver,3).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div[2]/div[2]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[1]/input"))
    )

    search_input.send_keys(search_term)
    time.sleep(1)
    search_input.send_keys(Keys.RETURN)

    print_button =  WebDriverWait(driver,3).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div[2]/div[2]/div[1]/div/div/div[3]/a"))
    )
    time.sleep(3)
    print_link = print_button.get_attribute("href")
    data_set["Report"] = print_link
    data_set['Filler_data'] = "someblank stuff so this is an iterable object"
    driver.quit()
    print(data_set)
    return(data_set)