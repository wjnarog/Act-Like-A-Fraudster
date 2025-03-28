from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re

debug = True

def search_boulder(query):
    data_set = {}
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get ("https://maps.boco.solutions/legacyps/")

    # Wait to allow the page to load
    time.sleep(2)
    # print(driver.page_source) 
    
    # enter desired address here
    search_term = query
    
    search_input = driver.find_element(By.ID, "searchField")
    search_input.clear()
    search_input.send_keys(search_term)
    time.sleep(3)
    search_input.send_keys(Keys.RETURN)
    
    time.sleep(3)
    
    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    
    property_details = {}
    
    
    account_num_elem = soup.find('span', class_='labelme', string="Account Number:")
    if account_num_elem:
            account_number = account_num_elem.find_next_sibling('span').text.strip()
            property_details['Account Number'] = account_number
    else:
            property_details['Account Number'] = "Not Found"
    
    owner_elem = soup.find('span', class_='labelme', string="Owner:")
    if owner_elem:
            owner = owner_elem.find_next_sibling('span').text.strip()
            property_details['Owner'] = owner
    else:
            property_details['Owner'] = "Not Found"
    
    mailing_addr_elem = soup.find('span', class_='labelme', string="Mailing Address:")
    if mailing_addr_elem:
            mailing_addr = mailing_addr_elem.find_next_sibling('span').text.strip()
            property_details["Owner's Mailing Address"] = mailing_addr
    else:
            property_details["Owner's Mailing Address"] = "Not Found"
    
    property_addr_elem = soup.find('span', class_='labelme', string="Property Address:")
    if property_addr_elem:
            property_addr = property_addr_elem.find_next_sibling('span').text.strip()
            property_details["Property Address"] = property_addr
    else:
            property_details["Property Address"] = "Not Found"
    
            
    city_elem = soup.find('span', class_='labelme', string="City:")
    if city_elem:
            city = city_elem.find_next_sibling('span').text.strip()
            state = city_elem.find_next_sibling('span').find_next_sibling('span').find_next_sibling('span').text.strip()
            property_details["City"] = city
            property_details["State"] = state
    else:
            property_details["City"] = "Not Found"
            property_details["State"] = "Not Found"
            
    zip_elem = soup.find('span', class_='labelme', string="Zip:")
    if zip_elem:
            zip_code = zip_elem.find_next_sibling('span').text.strip()
            property_details["Zip Code"] = zip_code
    else:
            property_details["Zip Code"] = "Not Found"
    
    parcel_num_elem = soup.find('span', class_='labelme', string="Parcel Number:")
    if parcel_num_elem:
            parcel_number = parcel_num_elem.find_next_sibling('span').text.strip()
            property_details["Parcel Number"] = parcel_number
    else:
            property_details["Parcel Number"] = "Not Found"

    subdivison_elem = soup.find('span', class_='labelme', string="Subdivision:")
    if subdivison_elem:
            subdivison = subdivison_elem.find_next_sibling('span').text.strip()
            property_details["Subdivision"] = subdivison
    else:
            property_details["Subdivision"] = "Not Found"
            
    market_area_elem = soup.find('span', class_='labelme', string="Market Area:")
    if market_area_elem:
            market_area = market_area_elem.find_next_sibling('span').text.strip()
            property_details["Market Area"] = market_area
    else:
            property_details["Market Area"] = "Not Found"


    sqft_elem = soup.find('span', class_='labelme', string="Square Feet:")
    if sqft_elem:
            sqft = sqft_elem.find_next_sibling('span').text.strip()
            property_details["Square Feet"] = sqft
    else:
            property_details["Square Feet"] = "Not Found"
            
    acres_elem = soup.find('span', class_='labelme', string="Acres:")
    if acres_elem:
            acres = acres_elem.find_next_sibling('span').text.strip()
            property_details["Acres"] = acres
    else:
            property_details["Acres"] = "Not Found"
            
    # Tax records could easily be found from this method in 'Assessments' tab
    property_values = {}
    
    rows1 = soup.find('tbody').find_all('tr')
    
    # Loop through the rows and extract values for Total, Structure, and Land
    for row_i in rows1:
        label = row_i.find('span', class_='embolden').text.strip()
        
        # Find the "Actual" value in the second <td>
        actual_value = row_i.find_all('td')[1].find('span', class_='ng-binding').text.strip()
        
        if label in ["Total:", "Structure:", "Land:"]:
            property_values[label] = actual_value
      
    print(property_values)      
    property_details["Total Value"] = property_values['Total:']
    property_details["Structure Value"] = property_values['Structure:']
    property_details["Land Value"] = property_values['Land:']

     
    #Estimate of taxes
    for row in soup.find_all('tr'):
        if row.find('td') and "Estimate of taxes" in row.find('td').text:
            tax_row = row
            break
    # Extract the tax value from the second <td>
    if tax_row:
        tax_estimate = tax_row.find_all('td')[1].text.strip()
    else:
        tax_estimate = "Estimate of taxes not found"
    
    property_details["Property tax estimate"] = tax_estimate
    
    
    
    class_elem = soup.find('span', class_='labelme', string="Class:")
    if class_elem:
            class_data = class_elem.find_next_sibling('span').text.strip()
            property_details["Class"] = class_data
    else:
            property_details["Class"] = "Not Found"
            
    build_year_elem = soup.find('span', class_='labelme', string="Built:")
    if build_year_elem:
            build_year = build_year_elem.find_next_sibling('span').text.strip()
            property_details["Built"] = build_year
    else:
            property_details["Built"] = "Not Found"
    
    tot_room_num_elem = soup.find('span', class_='labelme', string="Total:")
    if tot_room_num_elem:
            tot_room_num = tot_room_num_elem.find_next_sibling('span').text.strip()
            property_details["Number of rooms"] = tot_room_num
    else:
            property_details["Number of rooms"] = "Not Found"
            
    bedroom_num_elem = soup.find('span', class_='labelme', string="Bedrooms:")
    if bedroom_num_elem:
            bedroom_num = bedroom_num_elem.find_next_sibling('span').text.strip()
            property_details["Bedrooms"] = bedroom_num
    else:
            property_details["Bedrooms"] = "Not Found"
    
    full_bath_num_elem = soup.find('span', class_='labelme', string="Full Bath:")
    if full_bath_num_elem:
        full_bath_num = full_bath_num_elem.find_next_sibling('span').text.strip()
        property_details["Full Bath"] = full_bath_num
    else:
            property_details["Full Bath"] = "Not Found"
    
    three_qtr_bath_num_elem = soup.find('span', class_='labelme', string="3/4 Bath:")
    if three_qtr_bath_num_elem:
            three_qtr_bath_num = three_qtr_bath_num_elem.find_next_sibling('span').text.strip()
            property_details["3/4 Bath"] = three_qtr_bath_num
    else:
            property_details["3/4 Bath"] = "Not Found"
            
    half_bath_num_elem = soup.find('span', class_='labelme', string="Half Bath:")
    if half_bath_num_elem:
            half_bath_num = half_bath_num_elem.find_next_sibling('span').text.strip()
            property_details["Half Bath"] = half_bath_num
    else:
            property_details["Half Bath"] = "Not Found"
    
   
            
    # can grab sqft of each floor of the home
    
    
    #can find previous deed info on 'Deeds and Sales' tab
    #then use the following link to search up the deed by 'Reception Number'
    #https://boulder.co.publicsearch.us/search/advanced
    
    
    rows2 = soup.find_all('tr', attrs={"ng-repeat": "deed in deeds"})
    deed_numbers = []
    for row_j in rows2:
        deed_number = row_j.find('span', class_='ng-binding').text.strip()
        deed_numbers.append(deed_number)
        
    property_details["Deed Numbers"] = deed_numbers
    
    
    zoning_elem = soup.find('span', class_='labelme', string="Zoning:")
    if zoning_elem:
            zoning = zoning_elem.find_next_sibling('span').text.strip()
            property_details["Zoning"] = zoning
    else:
            property_details["Zoning"] = "Not Found"

    for key, value in property_details.items():
        data_set[key] = value
    if (debug):
        print(data_set)
    
    # Return the response as a JSON object
    return (data_set)
