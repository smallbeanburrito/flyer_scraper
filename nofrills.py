import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

def nofrills_scrape(driver):
    driver.get("https://www.nofrills.ca/print-flyer")

    driver.implicitly_wait(2)

    # exit popup if any
    try:
        pop_up = driver.find_element(By.CLASS_NAME, "modal-dialog__content")
        pop_up = pop_up.find_element(By.CLASS_NAME, "modal-dialog__content__close")
        pop_up.click()
    except:
        pass

    now = datetime.now()
    day = now.strftime('%A')
    wednesday = day == 'Wednesday'

    if wednesday:
        content = driver.find_element(By.CLASS_NAME, "flyers-and-deals-layout__content")
        content = content.find_element(By.TAG_NAME, "main")
        content = content.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(content.get_attribute("id"))
    else:
        # switch to navigation frame
        content = driver.find_element(By.CLASS_NAME, "flyers-and-deals-layout__content")
        content = content.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(content.get_attribute("id"))

        # open ads dropdown menu
        ad_menu = driver.find_element(By.CLASS_NAME, "flipp-drop-down-pub-container")
        ad_menu.click()

        # switch to menu frame
        driver.switch_to.parent_frame()
        ads = driver.find_elements(By.TAG_NAME, "iframe")

        driver.switch_to.frame(ads[1].get_attribute("id"))
        ads = driver.find_element(By.TAG_NAME, "ul")
        ads = ads.find_elements(By.TAG_NAME, "li")

        weekly_flyer = 0
        selected = False
        # find index of weekly flyer
        for index, ad in enumerate(ads):
            title = ad.find_element(By.CLASS_NAME, "flipp-publication-header")
            title = driver.execute_script("return arguments[0].innerHTML;", title)
            weekly = re.search("^Weekly", title)
            if weekly:
                weekly_flyer = index
                selected = ad.find_element(By.TAG_NAME, "flipp-publication").get_attribute("is-selected") == 'true'

        actions = ActionChains(driver)
        driver.execute_script("arguments[0].scrollIntoView();", ads[weekly_flyer])
        time.sleep(0.5)

        # select weekly flyer
        ad_html = ads[weekly_flyer].find_element(By.TAG_NAME, "a")
        ad_html.click()
        time.sleep(0.25)
    '''
    SCRAPING
    '''
    # locate items
    pages = driver.find_element(By.TAG_NAME, "flipp-router")
    pages = pages.find_element(By.CLASS_NAME, "sfml-wrapper")
    pages = pages.find_elements(By.TAG_NAME, "sfml-flyer-image")

    content = driver.page_source
    doc = BeautifulSoup(content, 'lxml')
    items = doc.find_all('sfml-flyer-image-a')

    for item in items:
        item_name = item['label']
        print(item_name)
        




