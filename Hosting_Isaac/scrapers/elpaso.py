def search_elpaso(query):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from bs4 import BeautifulSoup
    
    data_set = {}
    address_to_search = "2366 Mesa Crest Grv"
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
    search_box.send_keys(query)
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
    
    # Find the 'data-list-section' that contains the relevant data
    data_list_section = soup.find('div', class_='data-list-section')
    
    # Find all the list items (li) within this section
    data_rows = data_list_section.find_all('li', class_='clearfix data-list-row')
    
    property_details = {}
    
    # Iterate over each data row to extract the title and value
    for row in data_rows:
        title = row.find('span', class_='title')
        value = row.find('span', class_='value')
        
        # If the value is a dropdown (select), extract the selected option
        if not value:
            value = row.find('select')
            if value:
                value = value.find('option').text.strip()
        else:
            value = value.text.strip()
        
        if title and value:
            title_text = title.text.strip()
            property_details[title_text] = value
    
    # Print out the extracted data
    for key, value in property_details.items():
        data_set[key] = value
    # Find the "Market & Assessment Details" section
    assessment_section = soup.find('div', class_='assessment')
    
    # Find the data list containing market and assessed values
    data_list = assessment_section.find('ul', class_='data-list')
    
    # Extract the rows for the market and assessed values
    rows = data_list.find_all('li', class_='clearfix data-list-row')
    
    market_value = {}
    assessed_value = {}
    
    for row in rows:
        title = row.find('span', class_='title')
        value = row.find('span', class_='value')
        
        if title and value:
            title_text = title.text.strip()
            value_text = value.text.strip()
    
            # Checking if the title matches categories and storing the respective values
            if title_text in ["Land", "Improvement", "Total"]:
                market_value[title_text] = value_text
            if title_text in ["Land", "Improvement", "Total"]:
                assessed_value[title_text] = value_text
    
    # Print the results for Market and Assessed Values
    print("Market Value:")
    for key, val in market_value.items():
        data_set["Market Value "+key] = val
    
    print("\nAssessed Value:")
    for key, val in assessed_value.items():
        data_set["Assessed Key "+key] = val
    # Find the table containing the land details
    table = soup.find('table', class_='table-striped')
    
    # Extract the headers (columns) from the table
    headers = [th.text.strip() for th in table.find_all('th')]
    
    # Extract the rows of the table
    rows = table.find_all('tr')
    
    # Initialize an empty list to store dictionaries for each row
    data = []
    
    # Loop through each row (skipping the header row)
    for row in rows[1:]:
        columns = row.find_all('td')
        
        if columns:
            row_data = {}
            for i, col in enumerate(columns):
                # Assign the header as the key and the column value as the value
                row_data[headers[i]] = col.text.strip()
            data.append(row_data)
    
    # Now print the scraped land info in the format you requested
    index=0
    for land_info in data:
        data_set["landinfo"+str(index)] = land_info
        
        print(data_set)
    
    sections = soup.find_all('div', class_='panel panel-default')
    
    # Loop through each section and extract the details
    index = 0
    for section in sections:
        # Extract title for identification (either BI LEVEL 2 STORY or RESIDENTIAL OUTBUILDINGS)
        section_title = section.find('h4', class_='panel-title').get_text(strip=True)
    
        # Extract building details for each section
        market_value = section.find('div', class_='building-value').find_all('span')[1].get_text(strip=True)
        data_list = section.find('ul', class_='data-list')
        building_details = {}
    
        # Loop through each row and extract the title and value for each <p> tag
        for item in data_list.find_all('li', class_='data-list-row'):
            data_items = item.find_all('p', class_='data-list-item')
            for data_item in data_items:
                title_span = data_item.find('span', class_='title')
                value_span = data_item.find('span', class_='value')
    
                if title_span:
                    title = title_span.get_text(strip=True)
                    value = value_span.get_text(strip=True) if value_span else "-"
                    building_details[title] = value
        
        # Add the market value to the building details dictionary
        building_details['Market Value'] = market_value
    
        # Print out the details for each section
        # print(f"\n{section_title} Details:")
        # for key, value in building_details.items():
        #     print(f"{key}: {value}")
        data_set["Section"+str(index)] = building_details
        index += 1
    
    # Find the sales table
    sales_history = soup.find('div', id='sales')
    sales_table = sales_history.find_all('tr')
    
    # Initialize a list to store the sales data
    sales_data = []
    
    # Loop through each row in the sales table
    index = 0
    for row in sales_table:
        sale_info = {}
        
        # Extract the sale date, price, type, and reception from the main row
        columns = row.find_all('td')
        if len(columns) > 1:
            sale_date = columns[1].get_text(strip=True)
            sale_price = columns[2].get_text(strip=True)
            sale_type = columns[3].get_text(strip=True)
            reception = columns[4].get_text(strip=True)
            
            # Store the extracted information in the dictionary
            sale_info['Sale Date'] = sale_date
            sale_info['Sale Price'] = sale_price
            sale_info['Sale Type'] = sale_type
            sale_info['Reception'] = reception
            
            # Check for additional sale details if available (expand row button +)
            expand_row = columns[0].find('button')
            if expand_row:
                # Simulate a click to reveal additional information
                expand_button = driver.find_element(By.XPATH, f"//button[text()='+']")
                expand_button.click()
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "table-row-subdata-content"))
                )
                
                # Refresh the page source after expanding
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                
                # Re-locate the expanded data in the DOM
                expanded_row = soup.find_all('tr', class_='hide table-row-subdata')
    
                # Extract subdata for each expanded row
                if expanded_row:
                    subdata = expanded_row[0].find('ul', class_='data-list')
                    if subdata:
                        for item in subdata.find_all('li', class_='data-list-row'):
                            # Extract the title and value from each <p> tag
                            data_items = item.find_all('p', class_='data-list-item')
                            for data_item in data_items:
                                title_span = data_item.find('span', class_='title')
                                value_span = data_item.find('span', class_='value')
    
                                if title_span and value_span:
                                    title = title_span.get_text(strip=True)
                                    value = value_span.get_text(strip=True)
                                    sale_info[title] = value
                        
                        # Now, handle the Grantee field (dropdown)
                        grantee_select = subdata.find('select', class_='value')
                        if grantee_select:
                            # Get the first option in the dropdown, which is visible
                            selected_grantee = grantee_select.find('option')
                            if selected_grantee:
                                sale_info['Grantee'] = selected_grantee.get_text(strip=True)
            
            # Append the sale data to the list
            sales_data.append(sale_info)
    
    # Print the sales data in a cleaner format
    for sale in sales_data:
        data_set["Sale"+str(index)] = sale
        index += 1
        # for key, value in sale.items():
        #     print(f"{key}: {value}")
        # print()
    
    # Close the WebDriver
    # driver.quit()
    
    # Find the Tax Entity and Levy Information section
    tax_levy_section = soup.find('div', {'id': 'taxandlevytab'})
    
    # Extract the tax area code, levy year, and mill levy from the paragraph
    tax_info = tax_levy_section.find_all('p')[1].get_text(strip=True)
    data_set["TaxInfo"] = tax_info
    
    # Extract all rows from the Taxing Entity table
    table_rows = tax_levy_section.find_all('tr')
    
    # Initialize a list to store sales data
    sales_data = []
    
    # Extract and store the table data for each row
    for row in table_rows:
        cols = row.find_all('td')
        if len(cols) > 0:  # Skip empty rows
            sale = {
                "Taxing Entity": cols[0].get_text(strip=True),
                "Levy": cols[1].get_text(strip=True),
                "Contact Name/Organization": cols[2].get_text(strip=True),
                "Contact Phone": cols[3].get_text(strip=True)
            }
            sales_data.append(sale)
    
    # Print the sales data in the requested format
    index = 0
    for sale in sales_data:
        data_set["Tax"+str(index)] = sale
        # for key, value in sale.items():
        #     print(f"{key}: {value}")
        # print()
    
    # Find the MapSheet div
    map_sheet_div = soup.find('div', {'id': 'MapSheet'})
    
    # Find the <a> tag within the MapSheet div
    map_link = map_sheet_div.find('a')
    
    # Extract the href (link) and text from the <a> tag
    if map_link:
        map_url = map_link.get('href')
        map_text = map_link.get_text(strip=True)
        data_set["MapURL"] = map_url
        # print(f"Map Text: {map_text}")
    else:
        print("Map link not found.")
    
    # Close the driver
    driver.quit()
    
    return(data_set)