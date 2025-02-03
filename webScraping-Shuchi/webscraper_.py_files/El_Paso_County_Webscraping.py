from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_property_info(address_to_search):
    # Initialize the Chrome WebDriver and load the property search website
    driver = webdriver.Chrome()
    driver.get("https://property.spatialest.com/co/elpaso/#/")

    # Wait for the search box to be visible and input the address
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "primary_search"))
    )

    # Input the address to search for and submit the search
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'primary_search'))
    )
    search_box.send_keys(address_to_search)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load on the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "data-list-section"))
    )

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # --------------------------------------------
    # Extracting General Property Information
    # --------------------------------------------

    # Extract basic property details (address, owner, etc.)
    data_list_section = soup.find('div', class_='data-list-section')
    data_rows = data_list_section.find_all('li', class_='clearfix data-list-row')
    property_details = {}

    for row in data_rows:
        title = row.find('span', class_='title')
        value = row.find('span', class_='value') or row.find('select')
        if value:
            value = value.find('option').text.strip() if value.find('option') else value.text.strip()
        if title and value:
            property_details[title.text.strip().replace(':', '')] = value

    # Print extracted property details
    for key, value in property_details.items():
        print(f"{key}: {value}")

    # --------------------------------------------
    # Extracting Market & Assessed Values
    # --------------------------------------------

    # Extract Market and Assessed Values from the assessment section
    assessment_section = soup.find('div', class_='assessment')
    data_list = assessment_section.find('ul', class_='data-list')
    rows = data_list.find_all('li', class_='clearfix data-list-row')

    market_value, assessed_value = {}, {}

    for row in rows:
        title = row.find('span', class_='title')
        value = row.find('span', class_='value')
        if title and value:
            title_text = title.text.strip()
            value_text = value.text.strip()
            if title_text in ["Land", "Improvement", "Total"]:
                market_value[title_text] = value_text
                assessed_value[title_text] = value_text

    # Print Market & Assessed Values
    print("\nMarket & Assessment Details: ")
    print("Market Value:")
    for key, value in market_value.items():
        print(f"{key}: {value}")

    print("\nAssessed Value:")
    for key, value in assessed_value.items():
        print(f"{key}: {value}")

    # --------------------------------------------
    # Extracting Land Details
    # --------------------------------------------

    # Extract land details from the table
    table = soup.find('table', class_='table-striped')
    headers = [th.text.strip() for th in table.find_all('th')]
    rows = table.find_all('tr')

    land_data = []
    for row in rows[1:]:  # Skip the header row
        columns = row.find_all('td')
        if columns:
            row_data = {}
            for i, col in enumerate(columns):
                row_data[headers[i]] = col.text.strip()
            land_data.append(row_data)

    # Print Land Details
    print("\nLand Details:")
    for land_info in land_data:
        for key, value in land_info.items():
            print(f"{key}: {value}")
        print()

    # --------------------------------------------
    # Extracting Building Details
    # --------------------------------------------

    # Extract building information from the sections on the page
    sections = soup.find_all('div', class_='panel panel-default')

    print(f"Building Details:")
    for section in sections:
        # Extract title and market value for each building section
        section_title = section.find('h4', class_='panel-title').get_text(strip=True)
        market_value = section.find('div', class_='building-value').find_all('span')[1].get_text(strip=True)
        data_list = section.find('ul', class_='data-list')
        building_details = {}

        # Loop through each row to extract building title and value
        for item in data_list.find_all('li', class_='data-list-row'):
            data_items = item.find_all('p', class_='data-list-item')
            for data_item in data_items:
                title_span = data_item.find('span', class_='title')
                value_span = data_item.find('span', class_='value')

                if title_span:
                    title = title_span.get_text(strip=True)
                    value = value_span.get_text(strip=True) if value_span else "-"
                    building_details[title] = value
        
        # Add market value to building details
        building_details['Market Value'] = market_value

        # Print building details
        print(f"\n{section_title} Details:")
        for key, value in building_details.items():
            print(f"{key}: {value}")

    # --------------------------------------------
    # Extracting Sales History
    # --------------------------------------------

    # Extract sales history information from the page
    sales_history = soup.find('div', id='sales')
    sales_table = sales_history.find_all('tr')

    sales_data = []

    for row in sales_table:
        sale_info = {}
        columns = row.find_all('td')
        if len(columns) > 1:
            sale_date = columns[1].get_text(strip=True)
            sale_price = columns[2].get_text(strip=True)
            sale_type = columns[3].get_text(strip=True)
            reception = columns[4].get_text(strip=True)

            sale_info['Sale Date'] = sale_date
            sale_info['Sale Price'] = sale_price
            sale_info['Sale Type'] = sale_type
            sale_info['Reception'] = reception

            # Handle expanded sale details if available
            expand_row = columns[0].find('button')
            if expand_row:
                expand_button = driver.find_element(By.XPATH, f"//button[text()='+']")
                expand_button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "table-row-subdata-content"))
                )

                # Refresh the page source and extract expanded data
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                expanded_row = soup.find_all('tr', class_='hide table-row-subdata')
                if expanded_row:
                    subdata = expanded_row[0].find('ul', class_='data-list')
                    if subdata:
                        for item in subdata.find_all('li', class_='data-list-row'):
                            data_items = item.find_all('p', class_='data-list-item')
                            for data_item in data_items:
                                title_span = data_item.find('span', class_='title')
                                value_span = data_item.find('span', class_='value')

                                if title_span and value_span:
                                    title = title_span.get_text(strip=True)
                                    value = value_span.get_text(strip=True)
                                    sale_info[title] = value

                        # Extract the Grantee field if available
                        grantee_select = subdata.find('select', class_='value')
                        if grantee_select:
                            selected_grantee = grantee_select.find('option')
                            if selected_grantee:
                                sale_info['Grantee'] = selected_grantee.get_text(strip=True)

            sales_data.append(sale_info)

    # Print Sales History
    print("Sales History:")
    for sale in sales_data:
        for key, value in sale.items():
            print(f"{key}: {value}")
        print()

    # --------------------------------------------
    # Extracting Tax and Levy Information
    # --------------------------------------------

    # Extract tax and levy details from the page
    tax_levy_section = soup.find('div', {'id': 'taxandlevytab'})

    # Extract tax area code, levy year, and mill levy
    tax_info = tax_levy_section.find_all('p')[1].get_text(strip=True).replace(':', ': ').replace('Levy Year', ' \n   Levy Year').replace('Mill Levy', '\n   Mill Levy')
    print(f"Tax Information: \n   {tax_info} \n")

    # Extract Taxing Entity table rows
    table_rows = tax_levy_section.find_all('tr')

    tax_data = []
    for row in table_rows:
        cols = row.find_all('td')
        if len(cols) > 0:  # Skip empty rows
            tax_info = {
                "Taxing Entity": cols[0].get_text(strip=True),
                "Levy": cols[1].get_text(strip=True),
                "Contact Name/Organization": cols[2].get_text(strip=True),
                "Contact Phone": cols[3].get_text(strip=True)
            }
            tax_data.append(tax_info)

    # Print Taxing Entity and Levy Information
    print("\nTaxing Entity and Levy Information:")
    for tax in tax_data:
        for key, value in tax.items():
            print(f"{key}: {value}")
        print()

    # --------------------------------------------
    # Extracting Map Sheet Information
    # --------------------------------------------

    # Extract and print the URL for the map sheet link if available
    map_sheet_div = soup.find('div', {'id': 'MapSheet'})
    map_link = map_sheet_div.find('a')

    if map_link:
        map_url = map_link.get('href')
        print(f"Map URL: {map_url}")
    else:
        print("Map link not found.")
    print()

    # Clean up and close the driver
    driver.quit()

# Main function to run the scraper
if __name__ == "__main__":
    address = input("Enter the address to search for: ")
    scrape_property_info(address)
