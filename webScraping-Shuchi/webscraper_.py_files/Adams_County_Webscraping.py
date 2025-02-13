from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re


def scrape_property_info(address_to_search):
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    driver.get("https://gisapp.adcogov.org/PropertySearch")

    # Wait for the search box to be visible and locate it
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-text"))
    )

    # Send search query
    search_box.send_keys(address_to_search)
    search_box.send_keys(Keys.RETURN)

    # Wait for the table row containing the Parcel Number to be visible and clickable
    parcel_link = WebDriverWait(driver, 10).until(
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
    WebDriverWait(driver, 10).until(
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
        print(f"{key}: {value}")

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
        for row in rows:
            columns = row.find_all('td')
            account_summary_data["Account Number"] = columns[0].text.strip()
            account_summary_data["Date Added"] = columns[1].text.strip()
            account_summary_data["Tax District"] = columns[2].text.strip()
            account_summary_data["Mill Levy"] = columns[3].text.strip()

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
        else:
            print(f"{key}: {value}")

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
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"{key}: {value}")

    # --------------------------------------------
    # Sales Summary
    # --------------------------------------------

    print("\nSales Summary:")
    sales_table = soup.find('table', rules='all', border="2",
                            style="border-width:2px;border-style:Double;width:100%;page-break-inside:avoid;")
    rows = sales_table.find_all('tr')[1:]
    sale_data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 10:
            sale_dict = {
                'Sale Date': cells[0].find('span').get_text(strip=True) if cells[0].find('span') else '',
                'Sale Price': cells[1].find('span').get_text(strip=True) if cells[1].find('span') else '',
                'Deed Type': cells[2].find('span').get_text(strip=True) if cells[2].find('span') else '',
                'Reception Number': cells[3].find('span').get_text(strip=True) if cells[3].find('span') else '',
                'Book': cells[4].find('span').get_text(strip=True) if cells[4].find('span') else '',
                'Page': cells[5].find('span').get_text(strip=True) if cells[5].find('span') else '',
                'Grantor': cells[6].find('span').get_text(strip=True) if cells[6].find('span') else '',
                'Grantee': cells[7].find('span').get_text(strip=True) if cells[7].find('span') else '',
                'Doc. Fee': cells[8].find('span').get_text(strip=True) if cells[8].find('span') else '',
                'Doc. Date': cells[9].find('span').get_text(strip=True) if cells[9].find('span') else ''
            }
            sale_data.append(sale_dict)

    if sale_data:
        for sale in sale_data:
            for key, value in sale.items():
                print(f"{key}: {value}")
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
        print(f"{key} {value}")

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
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 0:
                    if columns[0].text.strip() and columns[0].text.strip() != "Land Subtotal:":
                        land_valuation_data["Account Number"] = columns[0].text.strip(
                        )
                        land_valuation_data["Land Type"] = columns[1].text.strip(
                        )
                        land_valuation_data["Unit of Measure"] = columns[2].text.strip(
                        )
                        land_valuation_data["Number of Units"] = columns[3].text.strip(
                        )
                        land_valuation_data["Fire District"] = columns[4].text.strip(
                        )
                        land_valuation_data["School District"] = columns[5].text.strip(
                        )
                        land_valuation_data["Vacant/Improved"] = columns[6].text.strip()
                        land_valuation_data["Actual Value"] = columns[7].text.strip(
                        )
                        land_valuation_data["Assessed Value"] = columns[8].text.strip(
                        )

    improvements_valuation_data = {}
    improvements_valuation_section = soup.find(
        'span', string="Improvements Valuation Summary")
    if improvements_valuation_section:
        improvements_valuation_table = improvements_valuation_section.find_next('table', {
                                                                                'rules': 'all'})
        if improvements_valuation_table:
            rows = improvements_valuation_table.find_all('tr')[1:]
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 1:
                    if columns[0].text.strip() and columns[0].text.strip() != "Improvements Subtotal:":
                        improvements_valuation_data["Account Number"] = columns[0].text.strip(
                        )
                        improvements_valuation_data["Actual Value"] = columns[1].text.strip(
                        )
                        improvements_valuation_data["Assessed Value"] = columns[2].text.strip(
                        )

    valuation_data = {
        "Land Valuation Summary": land_valuation_data,
        "Improvements Valuation Summary": improvements_valuation_data,
    }

    for key, value in valuation_data.items():
        print(f"{key}:")
        if isinstance(value, dict):  # Check if the value is a dictionary
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {sub_value}")
        else:
            print(f"  {value}")
        print()

    # --------------------------------------------
    # Enterprise Zone Summary
    # --------------------------------------------
    print("Enterprise Zone Summary:")
    # Find the div containing the "Property within Enterprise Zone" section
    enterprise_zone_section = soup.find(
        'span', {'class': 'EnterpriseZoneSection'})

    enterprise_zone_data = {}

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
        print(f"{key}: {value}")

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
                print(f"  District: {rep['District']}, Link: {rep['Link']}")
            if 'Precinct' in rep:
                print(f"  Precinct: {rep['Precinct']}")
            print()

    # --------------------------------------------
    # Zoning Section
    # --------------------------------------------

    print("Zoning Summary:")
    zoning_section = soup.find('div', {'class': 'ZoningSummary'})
    zoning_data = {}
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
        print(f"{key}: {value}")

    # Close the driver after scraping
    driver.quit()


# Main function to run the scraper
if __name__ == "__main__":
    address = input("Enter the address to search for: ")
    scrape_property_info(address)
