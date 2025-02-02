from selenium.webdriver.common.by import By

form_link = "https://forms.gle/Uhvuq3d3Pp6T7jKE6"
site_link = "https://appbrewery.github.io/Zillow-Clone/"


#####scraping property site
from bs4 import BeautifulSoup
import requests

response=requests.get(site_link)
website_html = response.text

soup = BeautifulSoup (website_html,"html.parser")

##get link, price, address into lists

list_price = []


##Cleaning price data
search_prices = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
for item in search_prices:
    #'$2,895+/mo' -> '$2,974'
    price = item.text.split("/")[0]
    price = price.split("+")[0]
    list_price.append(price)

search_links = soup.find_all(class_="StyledPropertyCardDataArea-anchor")

##list of links

list_links = [item.get("href") for item in search_links]

##list of addresses
list_address = []
for item in search_links:
    address = item.text.replace("|",",").strip()
    list_address.append(address)

#### bot to fill data
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options =chrome_options)

driver.get(form_link)

def submit(address,price,link):
    input_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_address.send_keys(address)
    input_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_price.send_keys(price)
    input_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    input_link.send_keys(link)

    submit_button = driver.find_element(By.CLASS_NAME, "NPEfkd")
    submit_button.click()
    time.sleep(1)
    submit_another = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
    submit_another.click()

## loop to enter data into google sheet
for x in range(len(list_price)):
    submit(list_address[x], list_price[x],list_links[x])
