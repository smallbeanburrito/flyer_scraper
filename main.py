from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

path = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)

driver.get("https://www.foodbasics.ca/flyer.en.html#menu")

menu = driver.find_element(By.CLASS_NAME, "tcStoreList")
menu.click()

location = driver.find_element(By.XPATH, "//*[@id='injectStoreList']/label[111]")
location.click()

driver.implicitly_wait(10)

flyer_menu = driver.find_element(By.ID, "saveSelectedStore")
flyer_menu.click()

driver.switch_to.frame("myTcFlyerFrame")

flyers = driver.find_element(By.CLASS_NAME, "flyer-carousel")
flyer = flyers.find_element(By.TAG_NAME, 'a')
flyer.click()

load_content = driver.find_element(By.CLASS_NAME, "flyer-content")

action = ActionChains(driver)

action.move_to_element(load_content).perform()

#load and scroll to each page of flyer
load_items = load_content.find_elements(By.CLASS_NAME, "section-container")


for content in load_items:
    try:
        action.move_to_element(content).perform()
    except:
        break
#need to pass in new loaded page to beautiful soup every time
    content = driver.page_source

    doc = BeautifulSoup(content, 'lxml')

    items = doc.find_all('div', class_="block")

    unique_items = []

    for item in items:
        unique_item = item.find('div', class_="product-container")
        print(unique_item)
        if unique_item is None:
            continue
        else:
            unique_items.append(unique_item)

product_info = []

for item in unique_items:
    product_name = item.find('p', class_="sr-only").text
    product_price = item.find_all('span')
    if len(product_price) == 0:
        price = "Buy two or more"
    elif len(product_price) == 1:
        price = product_price[0].text
    else:
        price = ""
        for product in product_price:
            price = price + product.text
    product = (product_name, price)
    product_info.append(product)
    print(product)




# use move to next sibling to load each block






