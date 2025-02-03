from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def scrape_property_info(address_to_search):
    # Initialize the WebDriver and load the page
    driver = webdriver.Chrome()
    driver.get("https://apps.douglas.co.us/assessor/web#/")

    # Wait for the search box to appear and input the address
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'app-input-debounce input[type="text"]'))
    )
    search_box.send_keys(address_to_search)
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load and click on the first row
    driver.implicitly_wait(5)
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.table-row'))
    )
    first_row = driver.find_element(By.CSS_SELECTOR, 'a.table-row')
    first_row.click()

    # Wait for the pop-up and close it
    wait = WebDriverWait(driver, 10)
    close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Close']")))
    close_button.click()

    # Wait for the Account Summary dropdown to expand
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='SummaryAccountInfo']//span[@class='bar faux-button']")))
    dropdown_button = driver.find_element(By.XPATH, "//div[@id='SummaryAccountInfo']//span[@class='bar faux-button']")
    dropdown_button.click()

    # Extract the page content
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize dictionaries for key-value pairs
    key_value_pairs = {}

    # Extract the toggle button and links
    toggle_button = soup.find('span', class_='ui-button-text')
    if toggle_button:
        key_value_pairs["Toggle Button"] = toggle_button.text.strip()

    links = soup.find_all('a', href=True)
    for link in links:
        link_text = link.get_text(strip=True)
        link_url = link['href']
        key_value_pairs[link_text] = f'<a href="{link_url}">{link_text}</a>'

    
    # --------------------------------------------
    # Account Summary
    # --------------------------------------------
    
    print("Account Summary:")
    # Extract account summary data
    dropdown_content = soup.find('div', id='SummaryAccountInfo').find('div', class_='dropdown-content')
    account_summary_pairs = {}

    rows = dropdown_content.find_all('div', class_='skinny-row')
    for row in rows:
        label = row.find('div', class_='col-xs-4').text.strip().replace(":", "") if row.find('div', class_='col-xs-4') else None
        value = row.find('div', class_='col-xs-8').text.strip() if row.find('div', class_='col-xs-8') else None
        if label and value:
            account_summary_pairs[label] = value

    # Print Account Summary data
    for key, value in account_summary_pairs.items():
        if key != 'Update Mailing Address':  # Skip "Update Mailing Address"
            print(f"{key}: {value}")

    # Extract additional information: Location Description, Owner Info, PLSS Location
    location_description = soup.find('div', string='Location Description').find_next('div').text.strip()
    print(f"\nLocation Description: {location_description}")

    owner_info_div = soup.find('div', string='Owner Info').find_next('div')
    owner_info_raw = owner_info_div.text.strip()
    owner_info_parts = owner_info_raw.split("\n")
    owner_name = owner_info_parts[0].strip()
    owner_address = " ".join(owner_info_parts[1:]).strip()

    if "Update Mailing Address" in owner_address:
        owner_address = owner_address.split("Update Mailing Address")[0].strip()

    print(f"\nOwner Info:")
    print(f"Owner Name: {owner_name}")
    print(f"Owner Address: {owner_address}")

    plss_location = soup.find('div', string='Public Land Survey System (PLSS) Location').find_next('div').text.strip()
    plss_location_cleaned = ' '.join(plss_location.split())
    plss_location_cleaned = plss_location_cleaned.replace("Quarter:", "\nQuarter:").replace("Section:", "\nSection:").replace("Township:", "\nTownship:").replace("Range:", "\nRange:")
    print(f"\nPLSS Location: {plss_location_cleaned}")

    # Extract Section PDF Map link
    section_pdf_map = None
    pdf_map_rows = soup.find_all('div', class_='skinny-row')
    for row in pdf_map_rows:
        link = row.find('a', href=True)
        if link and "SectionMap" in link['href']:
            section_pdf_map = link['href']
            break
    print(f"\nSection PDF Map Link: {section_pdf_map}")
    
    # --------------------------------------------
    # Valuation Information
    # --------------------------------------------
    print("\nValuation Information:")
    
    # Initialize a dictionary to store toggle button and links
    key_value_pairs = {}

    # Extract the toggle button text (Show Graphs)
    toggle_button = soup.find('span', class_='ui-button-text')
    if toggle_button:
        print(toggle_button.text.strip())  # Print 'Show Graphs'

    # Extract the anchor tags (links) and their href attributes
    links = soup.find_all('a', href=True)
    for link in links:
        link_text = link.get_text(strip=True)
        link_url = link['href']
        
        # Print specific links that we are interested in
        if link_text == "Get Taxes Due":
            print(f'{link_text}: {link_url}')  # Hyperlink Get Taxes Due
        elif link_text == "Property Tax Calculation":
            print(f'{link_text}: {link_url}')  # Hyperlink Property Tax Calculation

    # Now continue with the part for finding and processing the table data
    # Find the table with class 'value-data-table'
    table = soup.find('table', class_='value-data-table')
    if table:
        # print("Table found")  

        # Find all tbody elements inside the table with the 'sales-info' class, without specifying the dynamic part
        rows = table.find_all('tbody', class_='value-row')  

        # Check how many rows are found
        # print(f"Found {len(rows)} tbody elements.")  

        # Iterate over each row and extract data
        sales_data = []
        for row in rows:
            # Extract Year, Actual Value, Assessed Value, Tax Rate, Est. Tax Amount
            year = row.find_all('td')[0].text.strip() if len(row.find_all('td')) > 1 else None
            actual_value = row.find_all('td')[1].text.strip() if len(row.find_all('td')) > 1 else None
            assesssed_value = row.find_all('td')[2].text.strip() if len(row.find_all('td')) > 1 else None
            tax_rate = row.find_all('td')[3].text.strip() if len(row.find_all('td')) > 1 else None
            est_tax_amount = row.find_all('td')[4].text.strip() if len(row.find_all('td')) > 1 else None
        
            # Store row data in a dictionary
            row_data = {
                'Year': year,
                'Actual Value': actual_value,
                'Assessed Value': assesssed_value,
                'Tax Rate': tax_rate,
                'Est. Tax Amount': est_tax_amount
            }
            
            sales_data.append(row_data)

        # Print extracted data
        for row in sales_data:
            for key, value in row.items():
                print(f"{key}: {value}")
            print()

    else:
        print("Table not found.")
    
    # --------------------------------------------
    # Sales History
    # --------------------------------------------
    
    print("Sales History:")
    # Extract Sales Data
    table = soup.find('table', class_='sales-data-table table')
    links = soup.find_all('a', href=True)
    printed_links = set()

    for link in links:
        link_text = link.get_text(strip=True)
        link_url = link['href']

        if link_text == "View Neighborhood Sales" and link_url not in printed_links:
            print(f'{link_text}: {link_url}')
            printed_links.add(link_url)
        elif link_text == "Recorded Document Search" and link_url not in printed_links:
            print(f'{link_text}: {link_url}')
            printed_links.add(link_url)

    if table:
        rows = table.find_all('tbody', class_='sales-info')

        sales_data = []
        for row in rows:
            reception_no = row.find_all('td')[0].text.strip() if len(row.find_all('td')) > 0 else None
            sale_date = row.find_all('td')[1].text.strip() if len(row.find_all('td')) > 1 else None
            sale_price = row.find_all('td')[2].text.strip() if len(row.find_all('td')) > 1 else None
            deed_type = row.find_all('td')[3].text.strip() if len(row.find_all('td')) > 2 else None

            sales_details_row = row.find_next('tr', class_='sales-details')
            if sales_details_row:
                grantor_grantee_div = sales_details_row.find('div', class_='col-sm-9 col-xs-12')
                if grantor_grantee_div:
                    grantor = grantor_grantee_div.find_all('span', class_='ng-star-inserted')[0].text.strip().replace('Grantor:', '').strip()
                    grantee = grantor_grantee_div.find_all('span', class_='ng-star-inserted')[1].text.strip().replace('Grantee:', '').strip()
                else:
                    grantor, grantee = None, None
            else:
                grantor, grantee = None, None

            row_data = {
                'Reception No': reception_no,
                'Sale Date': sale_date,
                'Sale Price': sale_price,
                'Deed Type': deed_type,
                'Grantor': grantor,
                'Grantee': grantee
            }

            sales_data.append(row_data)

        for row in sales_data:
            print("\n")
            for key, value in row.items():
                print(f"{key}: {value}")
    else:
        print("Table not found.")
    
    # --------------------------------------------
    # Building Details
    # --------------------------------------------
    
    print("\nBuilding Details:")
    building_data = {}

    # Find the building details section using its ID
    building_details = soup.find('div', {'id': 'BuildingDetails'})

    if building_details:
        # Scrape building images
        images = building_details.find_all('img', class_='bordered')
        image_urls = [img['src'] for img in images if img.has_attr('src')]
        building_data['Images'] = image_urls
        
        # Scrape building primary info (property type, year built, etc.)
        building_info = building_details.find_all('div', class_='smart-table')
        primary_info = {}

        for info in building_info:
            # Find the label and value pairs for each group
            label_elements = info.find_all('div', recursive=False)
            
            # Ensure there are exactly two divs, one for the label and one for the value
            if len(label_elements) == 2:
                label = label_elements[0].text.strip().replace('\n', '').replace('\r', '')
                value = label_elements[1].text.strip().replace('\n', '').replace('\r', '')
                
                # Add the pair to the primary info dictionary
                primary_info[label] = value

        building_data['\nPrimary Info'] = primary_info

        
        # Scrape additional features and fixtures
        additional_features = []
        more_details = building_details.find_all('div', class_='skinny-row')
        for detail in more_details:
            name = detail.find('span', class_='name')
            value = detail.find('span', class_='value')
            if name and value:
                name_text = name.text.strip().replace('\n', ' ')
                value_text = value.text.strip().replace('\n', ' ')
                additional_features.append({name_text: value_text})
        
        building_data['\nAdditional Features'] = additional_features

    else:
        print("Building details section not found.")

    # Print the scraped data, each key-value pair on its own line
    for key, value in building_data.items():
        print(f"{key}:")
        if isinstance(value, list):
            for item in value:
                # If the value is a dictionary (for additional features)
                if isinstance(item, dict): 
                    for sub_key, sub_value in item.items():
                        print(f"  {sub_key} {sub_value}")
                else:
                    print(f"  {item}")
        else:
            # For primary info, print each label-value pair on a new line
            if key == '\nPrimary Info': 
                for label, value in value.items():
                    print(f"  {label} {value}")
            else:
                print(f"  {value}")

    # --------------------------------------------
    # Land Details
    # --------------------------------------------
    
    print("\nLand Details:")
    
    land_info = {}

    land_info_section = soup.find('div', {'id': 'LandInfoAndValue'})

    if land_info_section:
        land_details = land_info_section.find_all('div', class_='row')

        for detail in land_details:
            label = detail.find('div', class_='col-xs-3')
            value = detail.find('div', class_='col-xs-9')

            if label and value:
                label_text = label.text.strip().replace('\n', '').replace('\r', '')
                value_text = value.text.strip().replace('\n', '').replace('\r', '')
                land_info[label_text] = value_text

        valuation_section = land_info_section.find('div', class_='header')
        if valuation_section and 'Land Valuation' in valuation_section.text:
            valuation_row = land_info_section.find_all('div', class_='row')[-1]
            actual_value_label = valuation_row.find('div', class_='col-sm-3')
            actual_value = valuation_row.find('div', class_='col-sm-9')

            if actual_value_label and actual_value:
                land_info['Actual Value'] = actual_value.text.strip().replace('\n', '').replace('\r', '')

        for key, value in land_info.items():
            print(f"{key} {value}")

    # --------------------------------------------
    # Tax Authorities
    # --------------------------------------------
    
    print("\nTax Authorities:")
    table = soup.find('table', class_='tax-data-table table')

    if table:
        rows = table.find_all('tbody', class_='tax-info')

        tax_data = []
        for row in rows:
            tax_id = row.find_all('td')[0].text.strip() if len(row.find_all('td')) > 0 else None
            authority_name = row.find_all('td')[1].text.strip() if len(row.find_all('td')) > 1 else None
            mills = row.find_all('td')[2].text.strip() if len(row.find_all('td')) > 2 else None
            tax_rate = row.find_all('td')[3].text.strip() if len(row.find_all('td')) > 3 else None
            tax_amount = row.find_all('td')[4].text.strip() if len(row.find_all('td')) > 4 else None

            row_data = {
                'ID': tax_id,
                'Authority Name': authority_name,
                'Mills': mills,
                'Tax Rate': tax_rate,
                'Est. Tax Amount': tax_amount
            }

            tax_data.append(row_data)

        for row in tax_data:
            for key, value in row.items():
                print(f"{key}: {value}")
            print()
        # Extract Total Tax Authorities Data
        all_total_data = []
        total_row = table.find_all('tbody')[-1]

        if total_row:
            total_cells = total_row.find_all('td')
            if len(total_cells) >= 5:
                total_data = {
                    'Total Authorities': total_cells[1].text.strip(),
                    'Total Mills': total_cells[2].text.strip(),
                    'Total Tax Rate': total_cells[3].text.strip(),
                    'Total Tax Amount': total_cells[4].text.strip()
                }
                all_total_data.append(total_data)

        for row in all_total_data:
            for key, value in row.items():
                print(f"{key}: {value}")

    # --------------------------------------------
    # Documents
    # --------------------------------------------
    
    print("Documents")
    dropdown_content = soup.find('div', id='Documents').find('div', class_='dropdown-content')
    documents_list = dropdown_content.find_all('li', class_='ng-star-inserted') if dropdown_content else []

    if documents_list:
        document_data = {}

        for doc in documents_list:
            doc_name = doc.find('a').text.strip() if doc.find('a') else None
            size = doc.find('div', class_='col-sm-2')
            size = size.text.strip().replace('Size:', '').strip() if size else None
            last_modified = doc.find('div', class_='col-sm-4')
            last_modified = last_modified.text.strip().replace('Last Modified Date:', '').strip() if last_modified else None

            document_data[doc_name] = {
                'Size': size,
                'Last Modified Date': last_modified
            }

        for doc_name, details in document_data.items():
            print(f"\nDocument Name: {doc_name}")
            for key, value in details.items():
                print(f"  {key}: {value}")

    else:
        print("No documents found")

    # --------------------------------------------
    # Notifications
    # --------------------------------------------
    
    print("Notifications")
    dropdown_content = soup.find('div', id='TaxInformation').find('div', class_='dropdown-content')
    notifications_list = dropdown_content.find_all('div', class_='ng-star-inserted') if dropdown_content else []

    if notifications_list:
        notifications_data = []

        for notification in notifications_list:
            notification_text = notification.find('span').text.strip() if notification.find('span') else None
            notifications_data.append(notification_text)

        for index, notification in enumerate(notifications_data):
            print(f"\nNotification {notification}")
    else:
        print("No notifications found in the dropdown.")
        
    print()
    # Close the browser
    driver.quit()

# Main function to run the scraper
if __name__ == "__main__":
    # address = input("Enter the address to search for: ")
    address = "2719 Castle Glen Dr"
    scrape_property_info(address)
