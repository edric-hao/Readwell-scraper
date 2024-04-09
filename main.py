import csv
from bs4 import BeautifulSoup as bs
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from config import get

path = get('driver')
print(path)

def scrape_shelves():
    driver = webdriver.Chrome(executable_path=get('driver'))
    login(driver)
    driver.find_element(By.PARTIAL_LINK_TEXT, "Browse").click()
    driver.find_element(By.LINK_TEXT, "Lists").click()
    driver.find_element(By.LINK_TEXT, "More lists with recent activity…").click()
    shelves = []
    html = driver.page_source
    soup = bs(html, "html.parser")
    for shelf in soup.find_all('a', class_='listTitle'):
        shelves.append([shelf['href']])
    for i in range(99):
        driver.find_element(By.CLASS_NAME, "next_page").click()
        html = driver.page_source
        soup = bs(html, "html.parser")
        for shelf in soup.find_all('a', class_='listTitle'):
            shelves.append([shelf['href']])
    driver.quit()
    with open('goodreads/shelves.csv', mode='w', newline="", encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        for shelf in shelves:
            csv_writer.writerow(shelf)


def login(driver):
    driver.get(get('goodreads_website'))
    driver.find_element(By.LINK_TEXT, "Sign in").click()
    driver.find_element(By.LINK_TEXT, "Sign in with email").click()
    #driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(5)
    driver.find_element(By.NAME, "email").send_keys(get('email'))
    driver.find_element(By.NAME, "password").send_keys(get('password'))
    driver.find_element(By.ID, "signInSubmit").click()
    time.sleep(5)


scrape_shelves()
