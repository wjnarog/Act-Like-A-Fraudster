from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
from time import sleep

zillow = "https://www.zillow.com/boulder-co-80303/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22north%22%3A40.01836%2C%22south%22%3A39.877298%2C%22east%22%3A-105.13107%2C%22west%22%3A-105.280254%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A93355%2C%22regionType%22%3A7%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D"
zillowGeneric = "https://www.zillow.com/"
zillowSearch = "80303"
zillowList = "List-c11n-8-107-0__sc-1smrmqp-0 StyledSearchListWrapper-srp-8-107-0__sc-1ieen0c-0 jBzkcM gagHXc photo-cards photo-cards_extra-attribution"
zillowEntry = "ListItem-c11n-8-107-0__sc-13rwu5a-0 StyledListCardWrapper-srp-8-107-0__sc-wtsrtn-0 dAZKuw xoFGK"

driver = webdriver.Firefox()
driver.get(zillow)

# search_input = driver.find_element(By.ID, "__c11n_6ng6")
# search_input.clear()
# search_input.send_keys(zillowSearch)
# search_input.send_keys(Keys.RETURN)

soup2 = BeautifulSoup(driver.page_source, "html.parser")
# driver.quit()

results = soup2.find(class_=zillowList)
listings = results.find_all(class_=zillowEntry)
# print(listings[0].prettify())

counter = 0
for listing in listings:
    print("Property " + str(counter))
    listingPrice = listing.find(class_="PropertyCardWrapper__StyledPriceLine-srp-8-107-0__sc-16e8gqd-1 jQesdM")
    if listingPrice:
        print(listingPrice.text)

    counter+=1
print("end")