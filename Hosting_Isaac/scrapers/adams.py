from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import time
import re

def process_reception_number_Adams(reception_number):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get("https://recording.adcogov.org/landmarkweb")

    # Wait for the page to load completely
    wait = WebDriverWait(driver, 3)
    try:
        wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "divInside")))
        # print("Page loaded successfully.")
    except Exception as e:
        print(f"Error loading page: {e}")
        driver.quit()
        return

    # Locate the "Reception number" link by its span text "reception number"
    try:
        reception_number_link = driver.find_element(
            By.XPATH, "//span[text()='reception number']/preceding-sibling::a")
        reception_number_link.click()
        # print("Clicked 'Reception number' link.")
    except Exception as e:
        print(f"Error clicking 'Reception number' link: {e}")
        driver.quit()
        return

    # Wait for the modal to appear (or time out after 10 seconds)
    try:
        disclaimer_modal = wait.until(
            EC.presence_of_element_located((By.ID, "disclaimer")))
        accept_button = driver.find_element(By.ID, "idAcceptYes")
        accept_button.click()
        # print("Disclaimer modal accepted.")
    except Exception as e:
        print(f"Disclaimer modal did not appear or could not be accepted: {e}")

    # Process the reception number
    # print(f"Processing reception number: {reception_number}")

    try:
        # Wait for the dropdown to be present on the page
        dropdown = wait.until(EC.presence_of_element_located(
            (By.ID, "matchType-InstrumentNumber")))
        # print("Dropdown located.")

        # Use the Select class to interact with the dropdown
        select = Select(dropdown)
        select.select_by_value("2")  # Select the "Equals" option
        # print("Dropdown option selected.")

        # Enter the reception number
        input_field = driver.find_element(By.ID, "instrumentNumber")
        input_field.clear()
        input_field.send_keys(reception_number)
        # print("Reception number entered.")

        # Find the submit button and click it
        submit_button = driver.find_element(By.ID, "submit-InstrumentNumber")
        submit_button.click()
        # print("Submit button clicked.")

        # Wait for the results table to load
        try:
            table = wait.until(
                EC.presence_of_element_located((By.ID, "resultsTable")))
            # print("Results table loaded.")

            # Locate the first row in the results table
            row = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//tr[contains(@id, 'doc_')]")))
            # print("Row found.")

            # Scroll the row into view
            driver.execute_script("arguments[0].scrollIntoView(true);", row)
            time.sleep(1)  # Wait for the scroll to complete

            # Use ActionChains to click the row
            actions = ActionChains(driver)
            actions.move_to_element(row).click().perform()
            # print("Row clicked.")

            # Wait for the details page to load
            wait.until(EC.presence_of_element_located(
                (By.ID, "documentInformationParent")))
            # print("Details page loaded.")

            # Extract the image source
            image_element = wait.until(
                EC.presence_of_element_located((By.ID, "documentImageInner")))
            image_src = image_element.get_attribute("src")
            return image_src

        except Exception as e:
            print(
                f"Error processing results for reception number {reception_number}: {e}")

        # Navigate back to the search page for the next reception number
        # driver.back()

    except Exception as e:
        print(f"Error processing reception number {reception_number}: {e}")

    # Close the browser
    driver.quit()

def scrape_property_info(address_to_search):
    data_set = {}
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get("https://gisapp.adcogov.org/PropertySearch")

    # Wait for the search box to be visible and locate it
    search_box = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "search-text"))
    )

    # Send search query
    search_box.send_keys(address_to_search)
    search_box.send_keys(Keys.RETURN)

    # Wait for the table row containing the Parcel Number to be visible and clickable
    parcel_link = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//table[@class='table']//tr[2]//td[1]//a"))
    )

    # Click the Parcel Number link which opens a new tab
    parcel_link.click()

    # Wait for the new tab to open (wait until the number of windows (tabs) becomes 2)
    WebDriverWait(driver, 3).until(EC.number_of_windows_to_be(2))

    # Get all window handles (tabs)
    windows = driver.window_handles

    # Switch to the new tab (the last window handle)
    driver.switch_to.window(windows[-1])

    # Extract the parcel number from the new page (you can adjust the XPath as needed)
    parcel_number = driver.current_url.split('pid=')[1]

    # Construct the new URL for scraping
    new_url = f"https://gisapp.adcogov.org/QuickSearch/doreport.aspx?pid={parcel_number}"

    # Now, go to the new URL and scrape the data
    driver.get(new_url)

    # Wait for the page to load fully
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # Extract page source for scraping
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # --------------------------------------------
    # Parcel ID and Owner Information
    # --------------------------------------------

    print("Parcel ID and Owner Information: ")
    # Extract the Parcel Number using regex (13 digits)
    parcel_number_text = None
    parcel_number = soup.find('span', {'class': 'ParcelIDAndOwnerInformation'})
    if parcel_number:
        # Search for a 13-digit number in the text
        match = re.search(r'\d{13}', parcel_number.text.strip())
        if match:
            # Extract the matched 13-digit number
            parcel_number_text = match.group(0)
        else:
            parcel_number_text = "Parcel Number Not Found"
    else:
        parcel_number_text = "Parcel Number Not Found"

    # Extract Owner's Name
    owner_name = soup.find('span', {'id': 'ownerNameLabel'}).text.strip()

    # Extract Property Address
    property_address = soup.find(
        'td', {'id': 'propertyContentCell'}).text.strip()

    # Create a dictionary to store the data
    property_data = {
        "Parcel Number": parcel_number_text,
        "Owner Name": owner_name,
        "Property Address": property_address
    }

    # Output the dictionary
    for key, value in property_data.items():
        data_set[key] = value

    # --------------------------------------------
    # Account Summary
    # --------------------------------------------

    print("\nAccount Summary: ")
    account_summary_data = {}

    # Extract Legal Description
    legal_description_section = soup.find('div', {'id': 'Panel'})
    if legal_description_section:
        legal_description = legal_description_section.find_next(
            'div', {'class': 'SingleValueBoxElement'})
        if legal_description:
            legal_description = legal_description.text.strip()

    # Extract Subdivision Plat
    subdivision_plat_section = soup.find('span', string="Subdivision Plat")
    if subdivision_plat_section:
        subdivision_plat = subdivision_plat_section.find_next(
            'div', {'class': 'SingleValueBoxElement'})
        if subdivision_plat:
            subdivision_plat = subdivision_plat.text.strip()

    # Extract Account Summary Table
    account_summary_table = soup.find(
        'div', {'class': 'TaxAccountSummary'}).find('table')

    if account_summary_table:
        # Extract row data from the table
        rows = account_summary_table.find_all('tr')[1:]
        index = 0
        for row in rows:
            columns = row.find_all('td')
            account_summary_data["Account Number" + str(index)] = columns[0].text.strip()
            account_summary_data["Date Added"+ str(index)] = columns[1].text.strip()
            account_summary_data["Tax District"+ str(index)] = columns[2].text.strip()
            account_summary_data["Mill Levy"+ str(index)] = columns[3].text.strip()
            index+=1

    # Create a dictionary to store all the data
    property_data = {
        "Legal Description": legal_description if legal_description else "",
        "Subdivision Plat": subdivision_plat if subdivision_plat else "",
        "Account Summary": account_summary_data if account_summary_data else ""
    }

    # Output the dictionary, printing each item on a new line
    for key, value in property_data.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
                data_set[sub_key] = sub_value
        else:
            data_set[key] = value

    # --------------------------------------------
    # Permits
    # --------------------------------------------

    print("\nPermits:")
    permits = {}

    permit_cases_section = soup.find('span', string="Permit Cases")
    permit_cases_value = "Not Available"  # Default value

    if permit_cases_section:
        permit_cases_value = permit_cases_section.find_next(
            'div', {'class': 'MultiValueBoxElement'})
        if permit_cases_value:
            permit_cases_value = permit_cases_value.text.strip()

    permits["Permit Cases"] = permit_cases_value

    # Output the dictionary
    for key, value in permits.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                data_set[sub_key] = sub_value
        else:
            data_set[key] = value

    # --------------------------------------------
    # Sales Summary
    # --------------------------------------------

    print("\nSales Summary:")
    sales_table = soup.find('table', rules='all', border="2",
                            style="border-width:2px;border-style:Double;width:100%;page-break-inside:avoid;")
    rows = sales_table.find_all('tr')[1:]
    sale_data = []
    index = 0
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 10:
            sale_dict = {
                'Sale Date'+str(index): cells[0].find('span').get_text(strip=True) if cells[0].find('span') else '',
                'Sale Price'+str(index): cells[1].find('span').get_text(strip=True) if cells[1].find('span') else '',
                'Deed Type'+str(index): cells[2].find('span').get_text(strip=True) if cells[2].find('span') else '',
                'Reception Number'+str(index): cells[3].find('span').get_text(strip=True) if cells[3].find('span') else '',
                'Book'+str(index): cells[4].find('span').get_text(strip=True) if cells[4].find('span') else '',
                'Page'+str(index): cells[5].find('span').get_text(strip=True) if cells[5].find('span') else '',
                'Grantor'+str(index): cells[6].find('span').get_text(strip=True) if cells[6].find('span') else '',
                'Grantee'+str(index): cells[7].find('span').get_text(strip=True) if cells[7].find('span') else '',
                'Doc. Fee'+str(index): cells[8].find('span').get_text(strip=True) if cells[8].find('span') else '',
                'Doc. Date'+str(index): cells[9].find('span').get_text(strip=True) if cells[9].find('span') else ''
            }
            
            if ('Reception Number'+str(index) in sale_dict):
                reception_num = sale_dict['Reception Number'+str(index)]
                deed_link = process_reception_number_Adams(reception_num)
                sale_data.append({'deed'+str(index): deed_link})
                
            sale_data.append(sale_dict)
            index += 1

    if sale_data:
        for sale in sale_data:
            for key, value in sale.items():
                data_set[key] = value
            print()

    # --------------------------------------------
    # Building Summary
    # --------------------------------------------

    print("Building Summary:")
    building_section = soup.find('span', {'class': 'BuildingSummary'})

    building_data = {}

    # Extract the table with the building details
    table = building_section.find('table')

    # Loop through each row in the table to extract key-value pairs
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 1:
                label = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                building_data[label] = value

    for key, value in building_data.items():
        data_set[key] = value

    # --------------------------------------------
    # Valuation Summary
    # --------------------------------------------

    print("\nValuation Summary:")
    land_valuation_data = {}
    land_valuation_section = soup.find('span', string="Land Valuation Summary")
    if land_valuation_section:
        land_valuation_table = land_valuation_section.find_next(
            'table', {'rules': 'all'})
        if land_valuation_table:
            rows = land_valuation_table.find_all('tr')[1:]
            index = 0
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 0:
                    if columns[0].text.strip() and columns[0].text.strip() != "Land Subtotal:":
                        land_valuation_data["Account Number"+str(index)] = columns[0].text.strip(
                        )
                        land_valuation_data["Land Type"+str(index)] = columns[1].text.strip(
                        )
                        land_valuation_data["Unit of Measure"+str(index)] = columns[2].text.strip(
                        )
                        land_valuation_data["Number of Units"+str(index)] = columns[3].text.strip(
                        )
                        land_valuation_data["Fire District"+str(index)] = columns[4].text.strip(
                        )
                        land_valuation_data["School District"+str(index)] = columns[5].text.strip(
                        )
                        land_valuation_data["Vacant/Improved"+str(index)] = columns[6].text.strip()
                        land_valuation_data["Actual Value"+str(index)] = columns[7].text.strip(
                        )
                        land_valuation_data["Assessed Value"+str(index)] = columns[8].text.strip(
                        )
                index += 1

    improvements_valuation_data = {}
    improvements_valuation_section = soup.find(
        'span', string="Improvements Valuation Summary")
    if improvements_valuation_section:
        improvements_valuation_table = improvements_valuation_section.find_next('table', {
                                                                                'rules': 'all'})
        if improvements_valuation_table:
            rows = improvements_valuation_table.find_all('tr')[1:]
            index = 0
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 1:
                    if columns[0].text.strip() and columns[0].text.strip() != "Improvements Subtotal:":
                        improvements_valuation_data["Account Number"+str(index)] = columns[0].text.strip(
                        )
                        improvements_valuation_data["Actual Value"+str(index)] = columns[1].text.strip(
                        )
                        improvements_valuation_data["Assessed Value"+str(index)] = columns[2].text.strip(
                        )
                index += 1

    valuation_data = {
        "Land Valuation Summary": land_valuation_data,
        "Improvements Valuation Summary": improvements_valuation_data,
    }

    for key, value in valuation_data.items():
        print(f"{key}:")
        if isinstance(value, dict):  # Check if the value is a dictionary
            for sub_key, sub_value in value.items():
                data_set[sub_key] = sub_value
        else:
            print(f"  {value}")
            data_set[key] = value
        print()

    # --------------------------------------------
    # Enterprise Zone Summary
    # --------------------------------------------
    print("Enterprise Zone Summary:")
    # Find the div containing the "Property within Enterprise Zone" section
    enterprise_zone_section = soup.find(
        'span', {'class': 'EnterpriseZoneSection'})

    enterprise_zone_data = {}

    #Check if enterprise_zone_data was found
    if (enterprise_zone_section != None):
        # Extract the title of the section (e.g., "Property within Enterprise Zone")
        title = enterprise_zone_section.find(
            'span', {'id': 'Label'}).get_text(strip=True)
    
        # Extract the value (True/False) from the "SingleValueBoxElement" div
        value = enterprise_zone_section.find(
            'div', {'class': 'SingleValueBoxElement'}).find('span').get_text(strip=True)

        # Store the key-value pair in the dictionary
        enterprise_zone_data[title] = value

    # Output the results
    for key, value in enterprise_zone_data.items():
        data_set[key] = value

    # --------------------------------------------
    # Precincts and Legislative Representatives Summary
    # --------------------------------------------

    print("\nPrecincts and Legislative Representatives Summary: ")
    representatives_data = {}
    representative_sections = soup.find_all(
        'span', class_='PrecinctsLegislativeRepresentatives')
    for section in representative_sections:
        label_span = section.find('span', id='Label')
        if label_span:
            title = label_span.text.strip()
        else:
            title = "Unknown Representative"
        table = section.find('table')
        if table:
            for row in table.find_all('tr')[1:]:
                columns = row.find_all('td')
                if len(columns) > 1:
                    district = columns[0].text.strip()
                    link_to_rep = columns[1].find('a')['href']
                    if title not in representatives_data:
                        representatives_data[title] = []
                    representatives_data[title].append(
                        {'District': district, 'Link': link_to_rep})

        precinct_section = section.find(
            'span', style="font-family:VERDANA, ARIAL, HELVETICA, SANS-SERIF;font-size:10pt;font-weight:normal;color:#000000;")
        if precinct_section:
            precinct_value = precinct_section.text.strip()
            if title not in representatives_data:
                representatives_data[title] = []
            representatives_data[title].append({'Precinct': precinct_value})

    for title, reps in representatives_data.items():
        if title == "Unknown Representative":
            continue
        print(f"{title}:")
        
        for rep in reps:
            if 'District' in rep:
                data_set["District"+str(index)] = rep['District']
                data_set["Link"+str(index)] = rep['Link']
            if 'Precinct' in rep:
                data_set["Precinct"+str(index)] = rep['Precinct']
            print()

    # --------------------------------------------
    # Zoning Section
    # --------------------------------------------

    print("Zoning Summary:")
    zoning_section = soup.find('div', {'class': 'ZoningSummary'})
    zoning_data = {}
    #Check if Zoning section exists
    if (zoning_section != None):
        zoning_table = zoning_section.find('table')
        rows = zoning_table.find_all('tr')
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) == 2:
                zoning_authority = cols[0].get_text(strip=True)
                zoning = cols[1].get_text(strip=True)
                zoning_data["Zoning Authority"] = zoning_authority
                zoning_data["Zoning"] = zoning

    for key, value in zoning_data.items():
        data_set[key]= value

    # Close the driver after scraping
    driver.quit()

    print(data_set)
    return(data_set)