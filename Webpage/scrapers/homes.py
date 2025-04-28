from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time


def search_homes(county_to_search):
    data_set = {}
    
    # Initialize the browser
    driver = webdriver.Chrome()

    # Go to the website
    driver.get("https://www.homes.com/")  # Replace with the actual URL

    # Wait for the body tag to load to ensure the page is ready
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Locate the search box using the class name
    search_box = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "multiselect-search"))  # Adjust if needed
    )

    # Ensure the input is in view and interactable
    driver.execute_script("arguments[0].scrollIntoView();", search_box)

    # Send search query
    search_box.send_keys(county_to_search)
    search_box.send_keys(Keys.RETURN)

    # Wait for the initial results container to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "placardContainer"))
    )

    # Now capture the page source after the search has resulted in new content
    page_source = driver.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract the information from the placard-container
    property_list = []

    # Loop through each property placard on the page
    placards = soup.find_all('li', class_='placard-container')
    for placard in placards:
        # Initialize a dictionary to store the property details
        property_details = {}

        # Get the price
        price = placard.find('p', class_='price-container').text.strip()
        property_details['price'] = price

        # Extract property features
        details = placard.find('ul', class_='detailed-info-container')
        if details:
            features = details.find_all('li')
            for feature in features:
                text = feature.text.strip()
                if "Beds" in text:
                    property_details['beds'] = text
                elif "Baths" in text:
                    property_details['baths'] = text
                elif "Sq Ft" in text:
                    property_details['sq_ft'] = text

        # Extract the property address
        address = placard.find('p', class_='property-name').text.strip()
        property_details['address'] = address

        # Extract the description of the property
        description = placard.find(
            'p', class_='property-description').text.strip()
        property_details['description'] = description

        agent = placard.find('div', class_='agent-info-container')
        if agent:
            # Extract agent information
            agent_name = placard.find('p', class_='agent-name').text.strip()
            agency_name = placard.find('p', class_='agency-name').text.strip()
            agent_number = placard.find(
                'p', class_='agency-number').text.strip()

            property_details['Agent Name'] = agent_name
            property_details['Agency Number'] = agency_name
            property_details['Agent Number'] = agent_number

            # Store the property details in the list
            property_list.append(property_details)

    # Output the scraped information
    index = 0
    for property in property_list:
        data_set["property"+str(index)] = property
        index += 1
            
    driver.quit()
    return data_set