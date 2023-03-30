import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

def nofrills_scrape(driver):
    driver.get("https://www.nofrills.ca/print-flyer")

    driver.implicitly_wait(5)

    pop_up = driver.find_element(By.CLASS_NAME, "modal-dialog__content")
    pop_up = pop_up.find_element(By.CLASS_NAME, "modal-dialog__content__close")
    pop_up.click()

    content = driver.find_element(By.CLASS_NAME, "flyers-and-deals-layout__content")
    content = content.find_elements(By.TAG_NAME, "iframe")
    driver.switch_to.frame(content[1].get_attribute("id"))

    """
    # open ads dropdown menu
    ad_menu = driver.find_element(By.CLASS_NAME, "flipp-drop-down-pub-container")
    ad_menu.click()

    # switch to menu frame
    driver.switch_to.parent_frame()
    ads = driver.find_elements(By.TAG_NAME, "iframe")
    driver.switch_to.frame(ads[1].get_attribute("id"))
    ads = driver.find_elements(By.TAG_NAME, "li")

    # select ad 
    #ad = ads[0].find_element(By.XPATH, "/html/body/flipp-router/flipp-publicationselector-page/div/div[1]/flipp-publication-selector-tile/div/flipp-publications/div/ul/li[1]/flipp-publication/div/div[2]/a")
    # inside navbar iframe
    
    # switch to ad frame
    content = content.find_element(By.CLASS_NAME, "flipp-flyer")
    content = content.find_element(By.TAG_NAME, "main")
    content = content.find_element(By.TAG_NAME, "iframe")
    driver.switch_to.frame(content.get_attribute("id"))
    """

    #select_ad = driver.find_element(By.CLASS_NAME, "flipp-drop-down-pub-more-pubs")
    # locate items
    pages = driver.find_element(By.TAG_NAME, "flipp-router")
    pages = pages.find_element(By.CLASS_NAME, "sfml-wrapper")
    pages = pages.find_elements(By.TAG_NAME, "sfml-flyer-image")
    pages[0].click()

    action = ActionChains(driver)

    """
    for page in pages:
        load_items = page.find_elements(By.TAG_NAME, "sfml-flyer-image-a")
        for load_item in load_items:
            action.move_to_element(load_item).perform()
    """


    content = driver.page_source
    doc = BeautifulSoup(content, 'lxml')
    #print(doc)
    items = doc.find_all('sfml-flyer-image-a')
    #print(items)

    for item in items:
        item_name = item['label']
        print(item_name)



