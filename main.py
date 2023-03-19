import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from openpyxl import Workbook
from openpyxl.utils import get_column_letter

from bs4 import BeautifulSoup

ads = Workbook()
flyer_items = ads.active

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

driver.get("https://www.foodbasics.ca/flyer.en.html#menu")

menu = driver.find_element(By.CLASS_NAME, "tcStoreList")
menu.click()

# select store location
location = driver.find_element(By.XPATH, "//*[@id='injectStoreList']/label[111]")
location.click()

driver.implicitly_wait(2)

flyer_menu = driver.find_element(By.ID, "saveSelectedStore")
flyer_menu.click()

driver.switch_to.frame("myTcFlyerFrame")

flyers = driver.find_element(By.CLASS_NAME, "flyer-carousel")
flyer = flyers.find_element(By.TAG_NAME, 'a')
flyer.click()

load_content = driver.find_element(By.CLASS_NAME, "flyer-content")

action = ActionChains(driver)

action.move_to_element(load_content).perform()

# load and scroll to each page of flyer
load_items = load_content.find_elements(By.CLASS_NAME, "section-container")

for content in load_items:
    for load_item in content.find_elements(By.CLASS_NAME, "block"):
        try:
            action.move_to_element(load_item).perform()
        except:
            break

# pass in each loaded page to beautiful soup
content = driver.page_source
doc = BeautifulSoup(content, 'lxml')
items = doc.find_all('div', class_="block")

unique_items = []

for item in items:
    unique_item = item.find('div', class_="product-container")
    if unique_item is None:
        continue
    else:
        unique_items.append(unique_item)
    print(unique_item)
print()

product_info = []

for item in unique_items:
    product_name = item.find('p', class_="sr-only").text
    if product_name == ' ':
        continue
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

# save into excel
absRow = 2
for column in product_info:
    absCol = 1
    flyer_items[get_column_letter(absCol) + str(absRow)] = column[0]
    flyer_items[get_column_letter(absCol+1) + str(absRow)] = column[1]
    absRow = absRow + 1

ads.save("flyers.xlsx")







