from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re


def scrape_county_info(county_to_search):
    chrome_options = Options()

    # chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")  # Prevent bot detection
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    driver.get("https://www.redfin.com/")

    search_term = county_to_search

    # search_input = driver.find_element(By.ID, "search-box-input")
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "search-box-input"))
    )

    search_input.send_keys(search_term)

    search_input.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "bp-Homecard__Address"))
    )

    address_elements = driver.find_elements(
        By.CLASS_NAME, "bp-Homecard__Address")

    addresses = []

    for address in address_elements:
        address_text = address.text.strip()
        addresses.append(address_text)

    for index, address in enumerate(addresses, start=1):
        print(f"{index}. {address}")
        
    driver.quit()


# Main function to run the scraper
if __name__ == "__main__":
    # county = input("Enter the county to search for: ")
    county = "boulder co"
    scrape_county_info(county)
