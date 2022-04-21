from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import os
from selenium.webdriver.common.by import By
import re
import inactive_mods
import pandas as pd


def scrape_comments_link():

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_experimental_option("detach", True)
    s = Service(os.getcwd() + "\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()

    driver.get(r"https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F")

    driver.find_element(By.CLASS_NAME, "AnimatedForm__textInput").send_keys("Silent_Raspberry602", Keys.ENTER)

    driver.find_element(By.XPATH, "//*[@id='loginPassword']").send_keys("asdfhjkl", Keys.ENTER)

    time.sleep(5)

    # all links will be initially stored in this list
    comments_link = []
    for _ in inactive_mods.use_list():
        driver.get(f"https://www.reddit.com/{_}/")

        # for scrolling till the end of page
        len_of_page = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return "
            "len_of_page;")
        match = False
        while not match:
            last_count = len_of_page
            time.sleep(5)  # for properly loading after a scroll
            len_of_page = driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return "
                "len_of_page;")
            if last_count == len_of_page:
                match = True

        soup = BeautifulSoup(driver.page_source, 'lxml')

        for link in soup.find_all('a',
                                  attrs={'href': re.compile("^https://")}):
            # display the actual urls
            if "r/PaladinsRealm" + "/comments" in link.get("href"):
                temp = link.get("href").split()
                comments_link.append(temp)

    df = pd.DataFrame(comments_link)
    df.to_csv("comments_link.csv", index=False)


# temp = pd.read_excel("Reddit account.xlsx", usecols=["user Name", "Password"])
# us_name = pd.DataFrame(temp)
# temp_ = us_name.values.tolist()
# print(temp_)

