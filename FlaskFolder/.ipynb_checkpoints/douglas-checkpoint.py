from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def search_douglas(query): 
    data_set = {}
    # Initialize the WebDriver and load the page
    driver = webdriver.Chrome()
    driver.get("https://apps.douglas.co.us/assessor/web#/")

    # Wait for the search box to appear and input the address
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'app-input-debounce input[type="text"]'))
    )
    search_box.send_keys("1803 Lake Drive")
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load and click on the first row
    driver.implicitly_wait(5)
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.table-row'))
    # )
    # first_row = driver.find_element(By.CSS_SELECTOR, 'a.table-row')
    # first_row.click()

    # Wait for the pop-up and close it
    wait = WebDriverWait(driver, 10)
    close_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button/span[text()='Close']")))
    close_button.click()
    
    # Wait for the account summary section to be loaded
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='dropdown-content']")))
    
    # Extract HTML content
    html_content = driver.page_source
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract Toggle Button and Links before Account Summary
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize a dictionary to store toggle button and links
    key_value_pairs = {}
    
    # Extract the toggle button text (key) and status (value)
    toggle_button = soup.find('span', class_='ui-button-text')
    if toggle_button:
        key_value_pairs["Toggle Button"] = toggle_button.text.strip()
    
    # Extract the anchor tags (links) and their href attributes
    links = soup.find_all('a', href=True)
    for link in links:
        link_text = link.get_text(strip=True)
        link_url = link['href']
        key_value_pairs[link_text] = f'<a href="{link_url}">{link_text}</a>'
    
    # Now proceed with the Account Summary logic
    # Target the dropdown for Account Summary by using its ID
    dropdown_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='SummaryAccountInfo']//span[@class='bar faux-button']")))
    
    # Click the dropdown to expand it
    dropdown_button.click()
    
    # Wait for the Account Summary content to load
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='SummaryAccountInfo']//div[@class='dropdown-content']")))
    
    # Extract HTML content again after the dropdown is expanded
    html_content = driver.page_source
    
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the dropdown content specifically under the 'SummaryAccountInfo' ID
    dropdown_content = soup.find('div', id='SummaryAccountInfo').find('div', class_='dropdown-content')
    
    # Extract the key-value pairs from Account Summary
    account_summary_pairs = {}
    
    # Find all the rows with the class 'skinny-row' which contain the label and value pairs
    rows = dropdown_content.find_all('div', class_='skinny-row')
    
    for row in rows:
        # Extract the label (key) and value (value)
        label = row.find('div', class_='col-xs-4').text.strip() if row.find('div', class_='col-xs-4') else None
        value = row.find('div', class_='col-xs-8').text.strip() if row.find('div', class_='col-xs-8') else None
        
        # Add to dictionary if both label and value exist
        if label and value:
            account_summary_pairs[label] = value
    
    # Print the Account Summary key-value pairs
    print(f"Account Summary:")
    for key, value in account_summary_pairs.items():
        # Skip the "Update Mailing Address" entry
        if key != 'Update Mailing Address':
            print(f"{key}: {value}")
            data_set[key] = value
    
    # Extract additional data (Location Description, Owner Info, PLSS Location)
    location_description = soup.find('div', string='Location Description').find_next('div').text.strip()
    
    # For Owner Info, we need to extract and clean it
    owner_info_div = soup.find('div', string='Owner Info').find_next('div')
    
    # Extract owner name and address
    owner_info_raw = owner_info_div.text.strip()
    
    # Split owner info into lines
    owner_info_parts = owner_info_raw.split("\n")
    
    # Clean up and extract the name and address properly
    owner_name = owner_info_parts[0].strip() 
    owner_address = " ".join(owner_info_parts[1:]).strip()  
    
    # If "Update Mailing Address" appears in the address, remove it
    if "Update Mailing Address" in owner_address:
        owner_address = owner_address.split("Update Mailing Address")[0].strip()
    
    # Extract PLSS Location
    plss_location = soup.find('div', string='Public Land Survey System (PLSS) Location').find_next('div').text.strip()
    
    # Clean the PLSS Location
    plss_location_cleaned = ' '.join(plss_location.split())
    
    # Optionally, reformat for better readability (if you want to format it neatly)
    plss_location_cleaned = plss_location_cleaned.replace("Quarter:", "\nQuarter:").replace("Section:", "\nSection:").replace("Township:", "\nTownship:").replace("Range:", "\nRange:")
    
    # Extract the Section PDF Map link (if it exists)
    section_pdf_map = None
    
    # Find all the div elements with class 'skinny-row'
    pdf_map_rows = soup.find_all('div', class_='skinny-row')
    
    for row in pdf_map_rows:
        # Look for an anchor tag within the row
        link = row.find('a', href=True)
        if link and "SectionMap" in link['href']:  # Check if the href contains "SectionMap"
            section_pdf_map = link['href']
            break 
    
    # Print other extracted information
    print(f"\nLocation Description: {location_description}")
    data_set["Location Description"] = location_description
    print(f"\nOwner Info:")
    print(f"Owner Name: {owner_name}")
    data_set["Owner Name"] = owner_name
    print(f"Owner Address: {owner_address}")
    data_set["Owner Address"] = owner_address
    print(f"\nPublic Land Survey System (PLSS) Location: {plss_location_cleaned}")
    #data_set["PLSS Location"] = {plss_location_cleaned}
    print(f"\nSection PDF Map Link: {section_pdf_map}")
    #data_set["PDF Map Link"] = {section_pdf_map}
    
    print(data_set)
    
    # Close the browser
    # driver.quit()
    
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
            data_set[link_text] = link_url  # Hyperlink Get Taxes Due
        elif link_text == "Property Tax Calculation":
            data_set[link_text] = link_url  # Hyperlink Property Tax Calculation
    
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
        
            # Store row data in a table
            sales_data.append({
                'Year': year,
                'Actual Value': actual_value,
                'Assessed Value': assesssed_value,
                'Tax Rate': tax_rate,
                'Est. Tax Amount': est_tax_amount
            })
            
        # Print extracted data
        index = 0
        for row in sales_data:
            data_set["sale"+str(index)] = row
            index+=1
    
        print(data_set)
    
    else:
        print("Table not found.")
    
    # Find the table with class 'sales-data-table table'
    table = soup.find('table', class_='sales-data-table table')
    # Extract the anchor tags (links) and their href attributes
    
    links = soup.find_all('a', href=True)
    # Use a set to track printed links, avoid duplications
    printed_links = set()  
    
    for link in links:
        link_text = link.get_text(strip=True)
        link_url = link['href']
        
        # Print specific links that we are interested in, only if not already printed
        if link_text == "View Neighborhood Sales" and link_url not in printed_links:
            data_set[link_text] = link_url
            printed_links.add(link_url)  # Mark this link as printed
        elif link_text == "Recorded Document Search" and link_url not in printed_links:
            data_set[link_text] = link_url
            printed_links.add(link_url)
    
            
    if table:
        # print("Table found")  
        
        # Find all tbody elements inside the table with the 'sales-info' class, without specifying the dynamic part
        rows = table.find_all('tbody', class_='sales-info')  
        # print(f"Found {len(rows)} tbody elements.")  
        
        # Iterate over each row and extract data
        sales_data = []
        for row in rows:
            # Extract Reception No, Sale Date, Sale Price, Deed Type, etc.
            reception_no = row.find_all('td')[0].text.strip() if len(row.find_all('td')) > 0 else None
            
            sale_date = row.find_all('td')[1].text.strip() if len(row.find_all('td')) > 1 else None
            sale_price = row.find_all('td')[2].text.strip() if len(row.find_all('td')) > 1 else None
            deed_type = row.find_all('td')[3].text.strip() if len(row.find_all('td')) > 2 else None
            
            # Extract Grantor and Grantee
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
            
            # Store row data in a dictionary
            sales_data.append({
                'Reception No': reception_no,
                'Sale Date': sale_date,
                'Sale Price': sale_price,
                'Deed Type': deed_type,
                'Grantor': grantor,
                'Grantee': grantee
            })
            
        # Print extracted data
        index = 0
        for row in sales_data:
            data_set["sales_doc"+ str(index)] = row
            index += 1
            
    
    else:
        print("Table not found.")
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
                key, new_value = label.split(": ")
                data_set[key] = new_value.replace(' ', '')
                value = label_elements[1].text.strip().replace('\n', '').replace('\r', '')
                key, new_value = value.split(":")
                data_set[key] = new_value.replace(' ', '')
    
                
                
                # Add the pair to the primary info dictionary
                primary_info[label] = value
    
        building_data['Primary Info'] = primary_info
    
        
        # Scrape additional features and fixtures
        additional_features = []
        more_details = building_details.find_all('div', class_='skinny-row')
        for detail in more_details:
            name = detail.find('span', class_='name')
            value = detail.find('span', class_='value')
            if name and value:
                name_text = name.text.strip().replace('\n', ' ').replace('\r', '')
                value_text = value.text.strip().replace('\n', ' ').replace('\r', '')
                additional_features.append({name_text: value_text})
        
        building_data['Additional Features'] = additional_features
    
    else:
        print("Building details section not found.")
    
    index = 0
    for item in building_data['Images']:
        data_set["image"+str(index)] = item
        index += 1
    
    index = 0
    for item in building_data['Additional Features']:
        data_set["feature"+str(index)] = item
        index += 1
    
    
    # Print the scraped data, each key-value pair on its own line
    # for key, value in building_data.items():
    #     print(f"{key}:")
    #     if isinstance(value, list):
    #         for item in value:
    #             # If the value is a dictionary (for additional features)
    #             if isinstance(item, dict): 
    #                 for sub_key, sub_value in item.items():
    #                     print(f"  {sub_key} {sub_value}")
    #             else:
    #                 print(f"  {item}")
    #     else:
    #         # For primary info, print each label-value pair on a new line
    #         if key == '\nPrimary Info': 
    #             for label, value in value.items():
    #                 print(f"  {label} {value}")
    #         else:
    #             print(f"  {value}")
    
    # Close the browser after scraping
    driver.quit()
    
    land_info = {}
    
    # Find the "LandInfoAndValue" section
    land_info_section = soup.find('div', {'id': 'LandInfoAndValue'})
    
    if land_info_section:
        # Scrape Land Details (Land Type, Class Code, etc.)
        land_details = land_info_section.find_all('div', class_='row')
        
        for detail in land_details:
            label = detail.find('div', class_='col-xs-3')
            value = detail.find('div', class_='col-xs-9')
            
            if label and value:
                # Clean up label and value text
                label_text = label.text.strip().replace('\n', '').replace('\r', '')
                value_text = value.text.strip().replace('\n', '').replace('\r', '')
                
                # Add label-value pair to the dictionary
                land_info[label_text] = value_text
        
        # Scrape Land Valuation (Actual Value)
        valuation_section = land_info_section.find('div', class_='header')
        if valuation_section and 'Land Valuation' in valuation_section.text:
            # Last row is the valuation row
            valuation_row = land_info_section.find_all('div', class_='row')[-1]  
            actual_value_label = valuation_row.find('div', class_='col-sm-3')
            actual_value = valuation_row.find('div', class_='col-sm-9')
            
            if actual_value_label and actual_value:
                land_info['Actual Value'] = actual_value.text.strip().replace('\n', '').replace('\r', '')
    
    # Print the scraped land info
    for key, value in land_info.items():
        data_set[key] = value
    
    # Find the table with class 'tax-data-table table'
    table = soup.find('table', class_='tax-data-table table')
    
    if table:
        # Find all tbody elements inside the table with the 'tax-info' class (except the last 'total-row')
        rows = table.find_all('tbody', class_='tax-info')  
        
        sales_data = []
        for row in rows:
            # Extract data from the first row
            tax_id = row.find_all('td')[0].text.strip() if len(row.find_all('td')) > 0 else None
            authority_name = row.find_all('td')[1].text.strip() if len(row.find_all('td')) > 1 else None
            mills = row.find_all('td')[2].text.strip() if len(row.find_all('td')) > 2 else None
            tax_rate = row.find_all('td')[3].text.strip() if len(row.find_all('td')) > 3 else None
            tax_amount = row.find_all('td')[4].text.strip() if len(row.find_all('td')) > 4 else None
            
            # Store row data in a dictionary
            sales_data.append({
                'ID': tax_id,
                'Authority Name': authority_name,
                'Mills': mills,
                'Tax Rate': tax_rate,
                'Est. Tax Amount': tax_amount
            })
    
        index = 0
        # Print extracted data
        for row in sales_data:
            data_set["tax"+str(index)] = row
            index+=1
            
    else:
        print("Table not found.")
    
    dropdown_content = soup.find('div', id='Documents').find('div', class_='dropdown-content')
    
    # Find the list of documents inside the dropdown
    documents_list = dropdown_content.find_all('li', class_='ng-star-inserted') if dropdown_content else []
    
    if documents_list:
        # Initialize an empty dictionary to store document data
        document_data = {}
    
        # Iterate through each document item and extract the desired data
        for doc in documents_list:
            # Get document name (PDF filename)
            doc_name = doc.find('a').text.strip() if doc.find('a') else None
            
            # Get file size
            size = doc.find('div', class_='col-sm-2')
            size = size.text.strip().replace('Size:', '').strip() if size else None
            
            # Get last modified date
            last_modified = doc.find('div', class_='col-sm-4')
            last_modified = last_modified.text.strip().replace('Last Modified Date:', '').strip() if last_modified else None
            
            # Store the extracted data in the dictionary with document name as the key
            document_data[doc_name] = {
                'Name': doc_name,
                'Size': size,
                'Last Modified Date': last_modified
            }
    
        # Print the document data dictionary
        index = 0
        for doc_name, details in document_data.items():
            data_set["document"+str(index)] = details
            index += 1
            
    else:
        print("No documents found ")
    
    # Close the browser
    # driver.quit()

    return(data_set)