from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

debug = True

def search_denver(query):
    data_set = {}
    driver = webdriver.Chrome()
    driver.get("https://www.denvergov.org/Property/")
    
    time.sleep(2)
    
    search_term = query
    
    search_input = driver.find_element(By.ID, "search")
    search_input.send_keys(search_term)
    
    time.sleep(1)
    search_input.send_keys(Keys.RETURN)
    
    # Wait for the table to be visible
    results_table = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "results_table"))
    )
    
    # Wait for the first link to be clickable
    search_result_link = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "search-result-link"))
    )
    search_result_link = driver.find_element(By.CLASS_NAME, "search-result-link")
    # results_table = driver.find_element(By.ID, "results_table")
    if search_result_link :
        # search_result_link = results_table.find_element(By.CLASS_NAME, "search-result-link")
        search_result_link.click()
        
        time.sleep(5)
        
    else:
        print("No results found")
        
    html = driver.page_source
    soup1 = BeautifulSoup(html, "html.parser")

    property_details = {}
    
    
    
    # info_bar_table = soup.find("table", id="property-info-bar")
    
    # if info_bar_table:
        
    #     info_bar_headers = info_bar_table.find("thead").find_all("th")
        
    #     headers = {}
        
    #     for header in info_bar_headers:
    #         header.text.strip()
            
    #     row_data = []
    #     for row in info_bar_table.find("tbody").find_all("tr"):
    #         cells = row.find_all("td")
    #         for cell in cells:
    #             row_data.append(cell.text.strip())
                
    #             if len(row_data) == len(headers):
    #                 for key, value in zip(headers, row_data):
    #                     property_details[key] = value
    #             else:
    #                 print("lists not same length")
    #                 print(row_data)
    #                 print(headers)
    # else:
    #     print("No info bar found")
    
    property_table = soup1.find("table", class_="table-striped")
    property_rows = property_table.find_all("tr")
     
    for p_row in property_rows:
        cells = p_row.find_all("td")  
        for i in range(0, len(cells), 2):  
            key_raw = cells[i].text.strip()
            pkey = key_raw.replace(":", "") 
            
            if i + 1 < len(cells):
                # value = cells[i + 1].get_text(strip=True)
                value = cells[i + 1].text.strip()
            else:
                value = "Not Found"
            
            
            property_details[pkey] = value
        
        map_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li#property_map_link > a"))
    )

    href_link = map_link.get_attribute("href")
    
    
    if href_link:
        driver.get(href_link)
        
        # WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "property_map")) 
        #     )
    
    else:
        print("No map link found")
    
    
    WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "summary_map_div")) 
            )
    time.sleep(2)
    html = driver.page_source
    
    soup2 = BeautifulSoup(html, "html.parser")
    map_info_section = soup2.find("div", class_="contentPanel contentContainer")

    if map_info_section:
        for item in map_info_section.find_all("div", class_="item"):
            label = item.find("div", class_="label").text.strip()
    
            value = item.find("div", class_="value")
        
            if value:
                value_text = value.text.strip()
            else:
                value_text = "No value found"
    
            property_details[label] = value_text
    else:
        print("No map info section found")

    assessment_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li#Assessment > a"))
    )



    href_link = assessment_link.get_attribute("href")
    
    
    if href_link:
        driver.get(href_link)
    else:
        print("No map link found")
    
    
    WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "assessment_data")) 
            )
    time.sleep(2)
    html = driver.page_source
    
    soup3 = BeautifulSoup(html, "html.parser")

    assessment_details = []
    
    panels = soup3.find_all("div", class_="panel panel-primary")
    
    for panel in panels:
        year = panel.find("h4", class_="panel-title").text.strip()
        table = panel.find("table", class_="table table-striped")
        rows = table.find("tbody").find_all("tr")
        
        
        for row in rows:
            cells = row.find_all("td")
            property_type = cells[0].text.strip()
            actual = cells[1].text.strip()
            assessed = cells[2].text.strip()
            if len(cells) > 3:
                exempt = cells[3].text.strip()
            else:
                exempt = "Not Found"
    
            assessment_details.append({
                "Year": year,
                "Type": property_type,
                "Actual": actual,
                "Assessed": assessed,
                "Exempt": exempt
            })
            
    
    # print(assessment_details)
    for detail in assessment_details:
        for key, value in detail.items():
            data_set[key] = value

    chain_of_title_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "li#Chain_of_Title > a"))
    )

    href_link = chain_of_title_link.get_attribute("href")
    
    
    if href_link:
        driver.get(href_link)
    else:
        print("No map link found")
    
    
    # WebDriverWait(driver, 10).until(
    #             EC.presence_of_element_located((By.ID, "assessment_data")) 
    #         )
    time.sleep(2)
    html = driver.page_source
    
    soup4 = BeautifulSoup(html, "html.parser")
    chain_of_title_records = []
    
    table = soup4.find("table", class_="table table-striped sortable tablesorter tablesorter-default")
    rows = table.find("tbody").find_all("tr")
    
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 0:
            reception_number = cells[0].text.strip()
            reception_date = cells[1].text.strip()
            instrument = cells[2].text.strip()
            sale_date = cells[3].text.strip()
            sale_price = cells[4].text.strip()
            grantor = cells[5].text.strip()
            grantee = cells[6].text.strip()
            
            chain_of_title_records.append({
                "Reception Number": reception_number,
                "Reception Date": reception_date,
                "Instrument": instrument,
                "Sale Date": sale_date,
                "Sale Price": sale_price,
                "Grantor": grantor,
                "Grantee": grantee
            })
            
    for record in chain_of_title_records:
        for key, value in record.items():
            data_set[key] = value

    
    
    for key, value in property_details.items():
            data_set[key] = value

    # Return the response as a JSON object
    return (data_set)