from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os
import csv


def scrape_data():
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_experimental_option("detach", True)
    s = Service(os.getcwd() + "\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()
    driver.get("https://www.reddit.com/search/?q=%22Inactive%20mod%22")

    # for scrolling till the end of page
    len_of_page = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var len_of_page=document.body.scrollHeight;return len_of_page;")
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

    posts = []
    for mod in soup.find_all("h3", class_="_eYtD2XCVieq6emjKBH3m"):
        if "r/" in mod.string:
            posts.append(mod.string.split())

    inactive_mods = []

    for post in posts:
        for mod in post:
            if 'r/' in mod:
                if mod[-1] == "," or mod[-1] == "." or mod[-1] == ";" or mod[-1] == "-" \
                        or mod[-1] == "/" or mod[-1] == "]" or mod[-1] == ")":
                    mod = mod[:-1]
                if mod[0] != "r":
                    mod = mod[mod.index("r"):]
                inactive_mods.append(mod)

    df = pd.DataFrame(inactive_mods)
    df.to_csv("inactive_mods_list.csv", index=False)

    driver.close()


def use_list():
    """ returns the list of all the communities that have inactive mods"""
    file = open("inactive_mods_list.csv")
    csv_reader = csv.reader(file)
    rows = []
    csv_reader = [element for sublist in csv_reader for element in sublist]
    for mod in csv_reader:
        if mod != "0":
            rows.append(mod)
    return rows
