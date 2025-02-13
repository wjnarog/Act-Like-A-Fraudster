from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time


def scrape_property_info(address_to_search):
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
    # search_box.send_keys("577 N 96th St")
    search_box.send_keys(address_to_search)
    search_box.send_keys(Keys.RETURN)

    # Wait for the initial results container to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "placard-container"))  # Adjust as necessary
    )

    # Scroll to trigger more content loading if necessary
    def scroll_to_load_more():
        last_height = driver.execute_script(
            "return document.body.scrollHeight")

        while True:
            # Scroll down to the bottom
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load
            time.sleep(3)  # Adjust sleep time if necessary

            # Calculate new scroll height and compare with the last height
            new_height = driver.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break  # No more content to load
            last_height = new_height

    # Call the scroll function to load more results if applicable
    scroll_to_load_more()

    # Now capture the page source after the search has resulted in new content
    page_source = driver.page_source

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # --------------------------------------------
    # Overview
    # --------------------------------------------

    print("Overview:")

    # Initialize an empty dictionary to store the property information
    property_info = {}

    # Extract price
    # price_element = soup.find('span', {'class': 'property-info-price'})
    price_element = soup.find('span', {'id': 'price'})
    if price_element:
        property_info['price'] = price_element.text.strip()
    else:
        property_info['price'] = "Not listed for sale"

    # Extract address
    address_element = soup.find(
        'span', {'class': 'property-info-address-main'})
    if address_element:
        property_info['address'] = address_element.text.strip()
    else:
        property_info['address'] = "Address not available"

    # Extract city, state, and zip code
    city_state_zip_element = soup.find(
        'span', {'class': 'property-info-address-citystatezip'})
    if city_state_zip_element:
        property_info['city_state_zip'] = city_state_zip_element.text.strip()
    else:
        property_info['city_state_zip'] = "City, State, Zip not available"

    # Extract estimated payment
    estimated_payment_element = soup.find(
        'p', {'class': 'property-estimated-info'})
    if estimated_payment_element:
        property_info['estimated_payment'] = estimated_payment_element.text.strip()
    else:
        property_info['estimated_payment'] = "Estimated payment not available"

    # Extract total views
    total_views_element = soup.find('span', {'class': 'total-views'})
    if total_views_element:
        property_info['total_views'] = total_views_element.text.strip()
    else:
        property_info['total_views'] = "Total views not available"

    # Extract property features (beds, baths, sqft, price per sqft)
    # Find all features (since there's a divider, we can use this approach)
    features = soup.find_all('span', {'class': 'property-info-feature-detail'})
    for feature in features:
        feature_value = feature.text.strip()
        feature_label = feature.find_previous(
            'span', {'class': 'property-info-feature'}).text if feature.find_previous('span', {'class': 'property-info-feature'}) else ""

        if 'Beds' in feature_label:
            property_info['beds'] = feature_value
        elif 'Baths' in feature_label:
            property_info['baths'] = feature_value
        elif 'Sq Ft' in feature_label:
            property_info['sqft'] = feature_value
        elif 'Price per Sq Ft' in feature_label:
            property_info['price_per_sqft'] = feature_value

    # Print the extracted information on new lines
    for key, value in property_info.items():
        print(f"{key}: {value}")

    # --------------------------------------------
    # Highlights
    # --------------------------------------------

    print("\nHightlights:")

    # Find the highlights section
    highlights_section = soup.find('section', {'id': 'highlights-section'})

    if highlights_section:
        highlights_info = {}

        # Extract the highlight features
        highlights_list = highlights_section.find_all('li', class_='highlight')
        for highlight in highlights_list:
            # Get the feature name
            feature = highlight.find(
                'span', class_='highlight-value').text.strip()
            # The value can be the same as the key or customized if needed
            highlights_info[feature] = feature

        for key, value in highlights_info.items():
            # print(f"{key}: {value}")
            print(f"{key}")
    else:
        print("Highlight section not found on Homes.com for this property.")

    # --------------------------------------------
    # About this Home
    # --------------------------------------------

    print("\nAbout this Home:")
    # Find the About This Home section
    about_section = soup.find('section', {'id': 'about'})

    if about_section:
        # Extract the property description
        property_description = about_section.find('p', {'id': 'ldp-description-text'}).text.strip(
        ) if about_section.find('p', {'id': 'ldp-description-text'}) else "No description available"

        # Initialize the agent_info dictionary
        agent_info = {}

        # Extract agent name (if available)
        agent_name_element = about_section.find(
            'a', {'class': 'agent-information-fullname'})
        if agent_name_element:
            agent_name = agent_name_element.text.strip()
            agent_info['Agent Name'] = agent_name
        else:
            agent_info['Agent Name'] = "No agent information available"

        # Extract agency name (if available)
        agency_name_element = about_section.find(
            'span', {'class': 'agent-information-agency-name'})
        if agency_name_element:
            agency_name = agency_name_element.text.strip()
            agent_info['Agency'] = agency_name
        else:
            agent_info['Agency'] = "No agency information available"

        # Extract contact info (if available)
        contact_info_element = about_section.find(
            'span', {'class': 'agent-information-idx-contact'})
        if contact_info_element:
            contact_info = contact_info_element.text.strip()
            agent_info['Contact Info'] = contact_info
        else:
            agent_info['Contact Info'] = "No contact info available"

        # Extract license number (if available)
        license_number_element = about_section.find(
            'span', {'class': 'agent-information-license-number'})
        if license_number_element:
            license_number = license_number_element.text.strip()
            agent_info['License Number'] = license_number
        else:
            agent_info['License Number'] = "No license number available"

        # Extract agent image URL (if available)
        agent_image_element = about_section.find(
            'img', {'class': 'agent-brand-img'})
        agent_image_url = agent_image_element['src'] if agent_image_element else "No agent image available"

        print("Property Description:")
        print(property_description)

        print("\nAgent Information:")
        for key, value in agent_info.items():
            print(f"{key}: {value}")

        print("\nAgent Image URL:")
        print(agent_image_url)

    else:
        print("About this home section not found on Homes.com for this property.")

    # --------------------------------------------
    # Property Details
    # --------------------------------------------

    print("\nProperty Details:")
    # Try to find the amenities section
    amenities_section = soup.find('section', {'id': 'amenities-container'})

    if amenities_section:
        amenities_data = {}

        # Extract "Property Details" (inside the first feature-category)
        property_details_section = amenities_section.find_all(
            'div', {'class': 'feature-category feature-0'})[0]
        if property_details_section:
            # Find each subcategory within the "Property Details" section
            subcategories = property_details_section.find_all(
                'div', {'class': 'subcategory-container'})
            for subcategory in subcategories:
                amenity_name = subcategory.find(
                    'p', {'class': 'amenity-name'}).text.strip()
                amenities = subcategory.find(
                    'ul', {'class': 'amenities-list'}).find_all('li', {'class': 'amenities-detail'})
                amenity_details = [amenity.text.strip()
                                   for amenity in amenities]
                amenities_data[amenity_name] = amenity_details

        # Extract "Community Details" (inside the second feature-category)
        community_details_section = amenities_section.find_all(
            'div', {'class': 'feature-category'})[0]
        if community_details_section:
            # Find each subcategory within the "Community Details" section
            subcategories = community_details_section.find_all(
                'div', {'class': 'subcategory-container'})
            for subcategory in subcategories:
                amenity_name = subcategory.find(
                    'p', {'class': 'amenity-name'}).text.strip()
                amenities = subcategory.find(
                    'ul', {'class': 'amenities-list'}).find_all('li', {'class': 'amenities-detail'})
                amenity_details = [amenity.text.strip()
                                   for amenity in amenities]
                amenities_data[amenity_name] = amenity_details

        for key, value in amenities_data.items():
            print(f"{key}:")
            for item in value:
                print(f"   {item}")
    else:
        print("Amenities section not found on Homes.com for this property.")

    # --------------------------------------------
    # About the Neighborhood
    # --------------------------------------------

    print("\nAbout the Nieghborhood:")

    # Try to find the "About South Littleton" section
    neighborhood_section = soup.find(
        'section', {'id': 'neighborhood-container'})

    if neighborhood_section:
        # Extract the Neighborhood Description
        description = neighborhood_section.find(
            'div', {'id': 'neighborhood-description'})
        neighborhood_description = description.text.strip(
        ) if description else "No description available."

        # Extract the Neighborhood KPI
        neighborhood_kpi_cards = neighborhood_section.find_all(
            'div', {'class': 'neighborhood-kpi-card'})
        kpi_data = {}
        for card in neighborhood_kpi_cards:
            title = card.find(
                'p', {'class': 'neighborhood-kpi-card-title'}).text.strip()
            value = card.find(
                'p', {'class': 'neighborhood-kpi-card-text'}).text.strip()
            kpi_data[title] = value

        # Print the Neighborhood KPI
        print("Neighborhood Key Performance Indicators:")
        for key, value in kpi_data.items():
            print(f"{key}: {value}")

        # Extract Neighborhood Image URLs
        neighborhood_images = neighborhood_section.find_all(
            'div', {'class': 'neighborhood-image-container'})
        image_urls = []
        for image_container in neighborhood_images:
            # Use Selenium to get the actual image URLs from the 'src' attribute
            img_tag = image_container.find(
                'img', {'class': 'neighborhood-image'})
            if img_tag:
                image_urls.append(img_tag['src'])

        # Print the Neighborhood Image URLs
        print("\nNeighborhood Image URLs:")
        for i, url in enumerate(image_urls, start=1):
            print(f"Image {i}: {url}")

    else:
        print("Neighborhood details not found on Homes.com for this property.")

    # --------------------------------------------
    # Property History
    # --------------------------------------------

    print("\nProperty History:")

    # Find the property history table
    price_history_table = soup.find('table', {'class': 'price-table'})

    # Check if the property history table exists
    if price_history_table:
        # Initialize an empty list to store the property history data as key:value pairs
        property_history_data = []
        # Find all rows in the table body
        rows = price_history_table.find_all('tr', {'class': 'table-body-row'})

        # Iterate over each row and extract the relevant data
        for row in rows:
            # Extracting each cell's content
            date = row.find('th', {'scope': 'row'})
            event = row.find('td', {'class': 'price-event'})
            price = row.find('td', {'class': 'price-price'})
            change = row.find('td', {'class': 'price-change'})
            sq_ft_price = row.find('td', {'class': 'price-sq-ft'})

            # Create a dictionary to store the key:value pairs for this row
            history_entry = {
                "Date": date.text.strip() if date else "N/A",
                "Event": event.text.strip() if event else "N/A",
                "Price": price.text.strip() if price else "N/A",
                "Change": change.text.strip() if change else "N/A",
                "Sq Ft Price": sq_ft_price.text.strip() if sq_ft_price else "N/A"
            }

            # Append the dictionary to the list
            property_history_data.append(history_entry)

        for entry in property_history_data:
            for key, value in entry.items():
                print(f"{key}: {value}")
            print()

    else:
        print("Property history not found on Homes.com for this property.")

    # --------------------------------------------
    # About the Listing Agent
    # --------------------------------------------

    print("\nAbout the Listing Agent:")

    # Extract agent's name
    agent_name = soup.find('a', {'class': 'agent-name'})
    if agent_name:
        agent_info = {}

        agent_info["Agent Name"] = agent_name.text.strip(
        ) if agent_name else "N/A"

        # Extract the brokerage information
        brokerage_info = soup.find('p', {'class': 'brokerage-info'})
        agent_info["Brokerage"] = brokerage_info.text.strip(
        ) if brokerage_info else "N/A"

        # Extract the phone number
        phone_number = soup.find('a', {'class': 'agent-phone'})
        agent_info["Phone Number"] = phone_number.text.strip(
        ) if phone_number else "N/A"

        # Extract the agent's bio
        agent_bio = soup.find('p', {'class': 'agent-bio'})
        agent_info["Bio"] = agent_bio.text.strip() if agent_bio else "N/A"

        # Extract the agent's profile image URL
        agent_image = soup.find('img', {'class': 'agent-bio-image'})
        agent_info["Profile Image URL"] = agent_image['src'] if agent_image else "N/A"

        # Extract the agent's profile link
        profile_link = soup.find('a', {'class': 'view-agent-profile-btn'})
        agent_info["Profile Link"] = profile_link['href'] if profile_link else "N/A"

        # Output the results as key:value pairs in the desired format
        for key, value in agent_info.items():
            print(f"{key}: {value}")

    else:
        print("Agent information not found on Homes.com for this property.")

    # --------------------------------------------
    # Purchase History
    # --------------------------------------------
    print("\nDeed History:")

    # Find the deed history section
    deed_history_section = soup.find(
        'section', {'id': 'deed-history-container'})
    if deed_history_section:
        deed_history = {}

        # Find the deed table
        deed_table = deed_history_section.find(
            'table', {'class': 'deed-table'})
        if deed_table:
            # Find all rows in the deed table body
            rows = deed_table.find_all(
                'tr', {'class': 'table-body-row deed-table-body-row'})

            for row in rows:
                # Extract date
                date = row.find('th', {'scope': 'row'})
                if date:
                    deed_history['Date'] = date.text.strip()

                # Extract buyer
                buyer = row.find('td', {'class': 'deed-buyer'})
                if buyer:
                    deed_history['Buyer'] = buyer.text.strip()

                # Extract sale price
                sale_price = row.find('td', {'class': 'deed-sale-price'})
                if sale_price:
                    deed_history['Sale Price'] = sale_price.text.strip()

                # Extract title company
                title_company = row.find('td', {'class': 'deed-title-company'})
                if title_company:
                    deed_history['Title Company'] = title_company.text.strip()

    # Print the deed history information
    if deed_history:
        for key, value in deed_history.items():
            print(f"{key}: {value}")
    else:
        print("\nDeed History not found on Homes.com for this property.")

    # --------------------------------------------
    # Mortage History
    # --------------------------------------------

    print("\nMortgage History:")

    # Find all mortgage rows (each <tr> with class "table-body-row")
    mortgage_rows = soup.find_all('tr', class_='table-body-row')

    # Initialize an empty list to store mortgage data
    all_mortgage_data = []

    # Loop through each mortgage row and extract the details
    for mortgage_row in mortgage_rows:
        mortgage_data = {}

        # Extract Date (from the button with class 'shorter-date')
        date = mortgage_row.find('span', class_='shorter-date')
        if date:
            mortgage_data['Date'] = date.text.strip()

        # Extract Status (from <td> with class 'mortgage-status')
        status = mortgage_row.find('td', class_='mortgage-status')
        if status:
            mortgage_data['Status'] = status.text.strip()

        # Extract Borrower(s) (from <td> with class 'mortgage-borrower')
        borrower = mortgage_row.find('td', class_='mortgage-borrower')
        if borrower:
            mortgage_data['Borrowers'] = borrower.text.strip()

        # Extract Total Amount (from <td> with class 'mortgage-amount')
        amount = mortgage_row.find('td', class_='mortgage-amount')
        if amount:
            mortgage_data['Total Amount'] = amount.text.strip()

        # Extract detailed information from the property-history-drawer
        mortgage_detail = mortgage_row.find(
            'div', class_='property-history-drawer')

        if mortgage_detail:
            # Extract Outstanding Balance
            outstanding_balance = mortgage_detail.find(
                'p', text="Outstanding Balance")
            if outstanding_balance:
                mortgage_data['Outstanding Balance'] = outstanding_balance.find_next(
                    'p').text.strip()

            # Extract Lender(s)
            lenders = mortgage_detail.find('p', text="Lender(s)")
            if lenders:
                mortgage_data['Lenders'] = lenders.find_next('p').text.strip()

            # Extract Loan Type
            loan_type = mortgage_detail.find('p', text="Loan Type")
            if loan_type:
                mortgage_data['Loan Type'] = loan_type.find_next(
                    'p').text.strip()

            # Extract Loan Term
            loan_term = mortgage_detail.find('p', text="Loan Term")
            if loan_term:
                mortgage_data['Loan Term'] = loan_term.find_next(
                    'p').text.strip()

            # Extract Interest Rate
            interest_rate = mortgage_detail.find('p', text="Interest Rate")
            if interest_rate:
                mortgage_data['Interest Rate'] = interest_rate.find_next(
                    'p').text.strip()

            # Extract Borrower(s) (if they are listed in the subtable)
            borrowers_in_subtable = mortgage_detail.find(
                'p', text="Borrower(s)")
            if borrowers_in_subtable:
                mortgage_data['Borrowers in Subtable'] = borrowers_in_subtable.find_next(
                    'p').text.strip()

        # Append the extracted data for each row
        all_mortgage_data.append(mortgage_data)

    # Output the list of all mortgage data, skipping the first one
    for mortgage in all_mortgage_data[1:]:
        if mortgage:  # Make sure there's data to print
            print("Mortgage Data:")
            for key, value in mortgage.items():
                print(f"{key}: {value}")
            print()

    # --------------------------------------------
    # Tax History
    # --------------------------------------------

    print("\nTax History:")

    # Find the tax history table body
    tax_table_body = soup.find('tbody', class_='tax-table-body')

    if tax_table_body:
        # Find all the rows in the tax history table
        tax_rows = tax_table_body.find_all('tr', class_='table-body-row')

        # Initialize a list to store tax data
        tax_data = []
        # Loop through each row and extract data
        for row in tax_rows:
            # Initialize a dictionary to store the row's data
            tax_info = {}

            # Extract Year
            year = row.find('th', class_='tax-year')
            if year:
                tax_info['Year'] = year.text.strip()

            # Extract Tax Paid
            tax_paid = row.find('td', class_='tax-amount')
            if tax_paid:
                tax_info['Tax Paid'] = tax_paid.text.strip()

            # Extract Tax Assessment
            tax_assessment = row.find('td', class_='tax-assessment')
            if tax_assessment:
                tax_info['Tax Assessment'] = tax_assessment.text.strip()

            # Extract Land value
            tax_land = row.find('td', class_='tax-land')
            if tax_land:
                tax_info['Land'] = tax_land.text.strip()

            # Extract Improvement value
            tax_improvement = row.find('td', class_='tax-improvement')
            if tax_improvement:
                tax_info['Improvement'] = tax_improvement.text.strip()

            # Only add to list if the data is complete (not empty)
            if tax_info:
                tax_data.append(tax_info)

        # Print the extracted tax data
        print("Tax Data:")
        for tax in tax_data:
            for key, value in tax.items():
                print(f"{key}: {value}")
            print()
    else:
        print("Tax history not found on Homes.com for this property.")

    # --------------------------------------------
    # Owner History
    # --------------------------------------------

    print("\nOwner History:")

    # Find the ownership history container
    ownership_history = soup.find('section', id='ownership-history-container')

    if ownership_history:
        # Find all the accordion wrappers containing the ownership data
        accordion_wrappers = ownership_history.find_all(
            'div', class_='accordion-wrapper')

        # Loop through each accordion-wrapper to extract the relevant ownership data
        for accordion_wrapper in accordion_wrappers:
            # Find the accordion button inside the current accordion-wrapper
            accordion_button = accordion_wrapper.find(
                'div', class_='accordion-button')

            if accordion_button:
                # Extract basic ownership information (Date, Name, Owned For, Owner Type)
                date = accordion_button.find_all('span')[0].text.strip(
                ) if accordion_button.find_all('span') else "N/A"
                name = accordion_button.find_all('span')[1].text.strip() if len(
                    accordion_button.find_all('span')) > 1 else "N/A"
                owned_for = accordion_button.find_all('span')[2].text.strip() if len(
                    accordion_button.find_all('span')) > 2 else "N/A"
                owner_type = accordion_button.find_all('span')[3].text.strip() if len(
                    accordion_button.find_all('span')) > 3 else "N/A"

                # Print basic ownership information
                print("Basic Ownership Information:")
                print(f"Date: {date}")
                print(f"Name: {name}")
                print(f"Owned For: {owned_for}")
                print(f"Owner Type: {owner_type}")
                print()

                # Extract Purchase Details
                purchase_details_section = accordion_wrapper.find(
                    'div', id='purchase-details-ownership')
                purchase_details = {}

                if purchase_details_section:
                    # Extract individual purchase details
                    listed_on = purchase_details_section.find(
                        'div', string='Listed on')
                    closed_on = purchase_details_section.find(
                        'div', string='Closed on')
                    sold_by = purchase_details_section.find(
                        'div', string='Sold by')
                    bought_by = purchase_details_section.find(
                        'div', string='Bought by')
                    sellers_agent = purchase_details_section.find(
                        'div', string="Seller's Agent")
                    buyers_agent = purchase_details_section.find(
                        'div', string="Buyer's Agent")
                    list_price = purchase_details_section.find(
                        'div', string='List Price')
                    sold_price = purchase_details_section.find(
                        'div', string='Sold Price')
                    premium_discount = purchase_details_section.find(
                        'div', string='Premium/Discount to List')
                    total_days_on_market = purchase_details_section.find(
                        'div', string='Total Days on Market')
                    views = purchase_details_section.find(
                        'div', string='Views')
                    current_estimated_value = purchase_details_section.find(
                        'div', string='Current Estimated Value')

                    purchase_details['Listed on'] = listed_on.find_next(
                        'div', class_='ownership-category-value').text.strip() if listed_on else "N/A"
                    purchase_details['Closed on'] = closed_on.find_next(
                        'div', class_='ownership-category-value').text.strip() if closed_on else "N/A"
                    purchase_details['Sold by'] = sold_by.find_next(
                        'div', class_='ownership-category-value').text.strip() if sold_by else "N/A"
                    purchase_details['Bought by'] = bought_by.find_next(
                        'div', class_='ownership-category-value').text.strip() if bought_by else "N/A"
                    purchase_details['Seller\'s Agent'] = sellers_agent.find_next(
                        'div', class_='ownership-category-value').text.strip() if sellers_agent else "N/A"
                    purchase_details['Buyer\'s Agent'] = buyers_agent.find_next(
                        'div', class_='ownership-category-value').text.strip() if buyers_agent else "N/A"
                    purchase_details['List Price'] = list_price.find_next(
                        'div', class_='ownership-category-value').text.strip() if list_price else "N/A"
                    purchase_details['Sold Price'] = sold_price.find_next(
                        'div', class_='ownership-category-value').text.strip() if sold_price else "N/A"
                    purchase_details['Premium/Discount to List'] = premium_discount.find_next(
                        'div', class_='ownership-category-value').text.strip() if premium_discount else "N/A"
                    purchase_details['Total Days on Market'] = total_days_on_market.find_next(
                        'div', class_='ownership-category-value').text.strip() if total_days_on_market else "N/A"
                    purchase_details['Views'] = views.find_next(
                        'div', class_='ownership-category-value').text.strip() if views else "N/A"
                    purchase_details['Current Estimated Value'] = current_estimated_value.find_next(
                        'div', class_='ownership-category-value').text.strip() if current_estimated_value else "N/A"

                    # Print Purchase Details
                    print("Purchase Details:")
                    for key, value in purchase_details.items():
                        # if value != "N/A":
                        print(f"{key}: {value}")
                    print("")

                # Extract Home Financials
                home_financials_section = accordion_wrapper.find(
                    'div', id='home-financials-ownership')
                home_financials = {}

                if home_financials_section:
                    original_mortgage = home_financials_section.find(
                        'div', string='Original Mortgage')
                    interest_rate = home_financials_section.find(
                        'div', string='Interest Rate')

                    home_financials['Original Mortgage'] = original_mortgage.find_next(
                        'div', class_='ownership-category-value').text.strip() if original_mortgage else "N/A"
                    home_financials['Interest Rate'] = interest_rate.find_next(
                        'div', class_='ownership-category-value').text.strip() if interest_rate else "N/A"

                    # Print Home Financials
                    print("Home Financials:")
                    for key, value in home_financials.items():
                        # if value != "N/A":
                        print(f"{key}: {value}")
                    print("")

            else:
                print("No ownership data found in this accordion wrapper.")
    else:
        print("Ownership history not found on Homes.com for this property.")

    # --------------------------------------------
    # MLS Information
    # --------------------------------------------

    print("\nMLS Information:")

    # Extract MLS Source
    mls_source = soup.find('span', {'class': 'heavy'})

    if mls_source:
        mls_info = {}
        mls_info["MLS Source"] = mls_source.find_next(
            'span').text.strip() if mls_source else "N/A"

        # Extract MLS Number
        mls_number = soup.find('p', {'class': 'mls-number'})
        mls_info["MLS Number"] = mls_number.find('span').find_next(
            'span').text.strip() if mls_number else "N/A"

        # Extract MLS Image URL
        mls_image = soup.find('img', {'class': 'mls-image'})
        mls_info["MLS Image URL"] = mls_image['src'] if mls_image else "N/A"

        # Output the results as key:value pairs in the desired format
        for key, value in mls_info.items():
            print(f"{key}: {value}")
    else:
        print("MLS information not found on Homes.com for this property.")

    print()
    # Close the driver
    driver.quit()


# Main function to run the scraper
if __name__ == "__main__":
    address = input("Enter the address to search for: ")
    scrape_property_info(" " + address)
