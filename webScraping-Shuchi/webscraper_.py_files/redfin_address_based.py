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
import requests


def scrape_property_info(address_to_search):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument(
        "--disable-blink-features=AutomationControlled")  # Prevent bot detection
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    url = "https://www.redfin.com/"
    driver.get(url)

    search_term = address_to_search

    # search_input = driver.find_element(By.ID, "search-box-input")
    search_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "search-box-input"))
    )

    search_input.send_keys(search_term)

    search_input.send_keys(Keys.RETURN)

    property_details = {}

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "AgentInfoCard"))
    )

    agent_name = driver.find_element(
        By.CLASS_NAME, "agent-basic-details--heading").text.strip()
    property_details["Agent Name"] = agent_name

    brokerage_name = driver.find_element(
        By.CLASS_NAME, "agent-basic-details--broker").text
    property_details["Brokerage Name"] = brokerage_name
    contact_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "listingContactSection"))
    )

    # Contact info can range from email, phone, both, etc. its going to be hard to standardize
    # Maybe use regex to use it in the future
    contact_info = contact_section.text.replace("Contact: ", "").strip()
    property_details["Agent Contact Info"] = contact_info
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "ExpandableAmenitiesInfoRow"))
    )
    sections = driver.find_elements(
        By.CLASS_NAME, "ExpandableAmenitiesInfoRow")

    soup = BeautifulSoup(driver.page_source, "html.parser")

    amenity_groups = soup.find_all("div", class_="amenity-group")
    for group in amenity_groups:

        section_title_element = group.find(
            "div", class_="propertyDetailsHeader")
        section_title = section_title_element.get_text(
            strip=True) if section_title_element else "Unknown"

        details = group.find_all("li", class_="entryItem")
        # print(f"Found {len(details)} details in section '{section_title}'")

        for detail in details:
            label_element = detail.find("span", class_="entryItemContent")

            if label_element:
                # print(f"Label Element Found: {label_element.text}")  # Debugging
                label = label_element.text.split(":")[0]

                spans = label_element.find_all("span")
                # print(f"Found {len(spans)} spans in label")  # Debuggig

                if len(spans) > 0:
                    # Last span is the value
                    detail_value = spans[-1].get_text(strip=True)
                    property_details[label] = detail_value
                else:
                    print(
                        f"Skipping detail (Not enough spans): {label_element.text}")

            else:
                print("Skipping detail (Label element not found)")

    for key, value in property_details.items():
        print(f"{key}: {value}")


# Main function to run the scraper
if __name__ == "__main__":
    # address = input("Enter the address to search for: ")
    address = "831 Crescent Dr, Boulder, CO 80303"
    scrape_property_info(address)
