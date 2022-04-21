from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import sys
import re
import subprocess
import os
import random
import inactive_mods
import comments
import pandas
import recent_posts
from comment_content import get_comment_content

n = len(pandas.read_csv("comments.csv"))  # number of rows in comments.csv


def open_browser():
    """opens the browser and returns the driver instance"""

    options = Options()
    options.add_argument("--disable-notifications")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", prefs)

    # # for opening your default browser
    # options.add_argument(
    #     "--user-data-dir=C:\\Users\\mudas\\AppData\\Local\\Google\\Chrome\\User Data")
    # options.add_argument("--profile-directory=Default")

    options.add_experimental_option("detach", True)
    s = Service(os.getcwd() + "\\chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.maximize_window()

    return driver


# where n is the total number of rows in comments_link.csv
def selected_link(n, name):
    """reads only a x number of entries from the comments list"""

    skip = sorted(random.sample(range(n), n - 1))
    df = pandas.read_csv(f"{name}.csv", skiprows=skip)
    return str(list(df)[0])


def install_packages():
    packages_used = ["selenium", "bs4", "pandas", "spintax", "requests"]
    for package in packages_used:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])


def karma_farming(driver, username, password, sub_reddit, title, text, url, flair, comment):
    """ for posting and commenting, you need to provide the driver through which it'll perform th actions,
    the username, password, sub-reddit, title, text, link, flair and comment"""

    # make sure to update this thousand to the number of rows you have in comments_link.csv
    comment_link = selected_link(1000, "comments_link")
    try:
        format = 0

        driver.get(r"https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F")

        driver.find_element(By.CLASS_NAME, "AnimatedForm__textInput").send_keys(username, Keys.ENTER)

        driver.find_element(By.XPATH, "//*[@id='loginPassword']").send_keys(password, Keys.ENTER)

        time.sleep(5)

        driver.get("https://www.reddit.com/submit")

        # for the sub reddit selection
        driver.find_element(By.CLASS_NAME, "_1MHSX9NVr4C2QxH2dMcg4M").send_keys(sub_reddit)

        # for title
        title_input = driver.find_element(By.XPATH, "//div[@class ='_3w_665DK_NH7yIsRMuZkqB']"
                                                    "/div[2]/div/div/textarea")
        title_input.click()
        title_input.send_keys(title)

        # for text of the content
        text_input = driver.find_element(By.XPATH, "//div[@class = '_3w_665DK_NH7yIsRMuZkqB']"
                                                   "/div[2]/div[2]/div/div/div[3]/div/div/div/"
                                                   "div/div/div/div/div/div")
        text_input.click()
        text_input.send_keys(text)

        # for clicking on link button
        driver.find_element(By.XPATH, "//div[@class ='_3w_665DK_NH7yIsRMuZkqB']/div/div/button[3]").click()

        # for url
        url_input = driver.find_element(By.XPATH, "//div[@class ='_3w_665DK_NH7yIsRMuZkqB']/div/div[2]/textarea")
        url_input.send_keys(url)

        # for flair button
        flair_btn = driver.find_element(By.XPATH, "//div[@class ='_3w_665DK_NH7yIsRMuZkqB']/div[3]/div/div/button[4]")
        time.sleep(6)

        # checking whether flair-button is enabled
        if flair_btn.is_enabled():

            flair_btn.click()
            time.sleep(2)
            try:
                flair_search = driver.find_element(By.XPATH, f"//div[@class = 'subredditvars-r-{sub_reddit[2:]}'][4]"
                                                             "/div/div/div/div/div/div/input")
                format += 1
            except Exception:
                flair_search = driver.find_element(By.XPATH, "//input[@class = '_1nQbRaoAvb6Uy0oI-OfDtZ']")
                format += 2

            flair_search.click()
            flair_search.send_keys(flair)

            if format == 1:
                try:
                    flair_select = driver.find_element(By.XPATH,
                                                       f"//div[@class = 'subredditvars-r-{sub_reddit[2:]}'][4]"
                                                       f"/div/div/div/div/div/div/div")
                    flair_select.click()
                    time.sleep(2)
                    driver.find_element(By.XPATH, "//button[@class='_2X1FFYUx3jzlnbcegBC_Sr _2iuoyPiKHN3kfOoeIQalDT "
                                                  "_10BQ7pjWbeYP63SAPNS8Ts HNozj_dKjQZ59ZsfEegz8']").click()

                except Exception:

                    print("That flair was not available")
                    driver.find_element(By.XPATH, "//button[@ class = 'qYzY57HWQ8W424hj3s10-']").click()

            elif format == 2:
                try:
                    flair_select = driver.find_element(By.XPATH,
                                                       "//div[@ class = '_3nRJIwLuth2pKYrXnr2jPN']/div/div/div[2]")
                    flair_select.click()
                    time.sleep(2)
                    driver.find_element(By.XPATH, "//button[@class = '_2iuoyPiKHN3kfOoeIQalDT "
                                                  "_10BQ7pjWbeYP63SAPNS8Ts HNozj_dKjQZ59ZsfEegz8 ']").click()
                except Exception:

                    print("That flair was not available")
                    driver.find_element(By.XPATH, "//button[@ class = 'qYzY57HWQ8W424hj3s10-']").click()

        time.sleep(3)
        try:
            done_btn = driver.find_element(By.XPATH, "//button[@class = '_18Bo5Wuo3tMV-RDB8-kh8Z "
                                                     "_2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts "
                                                     "HNozj_dKjQZ59ZsfEegz8 ']")
            done_btn.click()

        except Exception:
            print(f"Only approved users can post in {sub_reddit}")

            driver.find_element(By.XPATH, "// *[ @ id = 'SHORTCUT_FOCUSABLE_DIV'] "
                                          "/ div[2] / div / div / div / div[2] / div[3] / div[1] / div[2] / div[3] / "
                                          "div[3] / div[2] / div / div[1] / button").click()
            time.sleep(2)
            driver.find_element(By.XPATH, "//*[@id='SHORTCUT_FOCUSABLE_DIV']"
                                          "/div[4]/div/div/section/footer/button[2]").click()
            time.sleep(3)
            driver.find_element(By.XPATH, "//*[@id='SHORTCUT_FOCUSABLE_DIV']"
                                          "/div[4]/div/div/section/footer/button").click()

        else:
            print(f"\nsuccessfully posted in {sub_reddit}")

    except Exception:
        print(f"The account {username} has been used many times, "
              f"thus cannot further comment till a certain time has passed")

    try:
        try:
            time.sleep(7)

            # selects a totally random url from the huge comments_link.csv
            driver.get(comment_link)
            driver.implicitly_wait(2)
            comment_box = driver.find_element(By.XPATH, "//div[@class = 'DraftEditor-root']/div/div")
            actions = ActionChains(driver)
            actions.move_to_element(comment_box).perform()
            comment_box.click()
            comment_box.send_keys(comment)

            driver.find_element(By.XPATH, "//button[@class = '_22S4OsoDdOqiM-hPTeOURa "
                                          "_2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts "
                                          "_3uJP0daPEH2plzVEYyTdaH ']").click()

            print(f"\nSuccessfully commented on {comment_link}")

        except Exception:
            print(f"Couldn't post in {sub_reddit}")

            driver.get(comment_link)
            time.sleep(5)
            Alert(driver).accept()
            driver.implicitly_wait(2)
            comment_box = driver.find_element(By.XPATH, "//div[@class = 'DraftEditor-root']/div/div")
            actions = ActionChains(driver)
            actions.move_to_element(comment_box).perform()
            comment_box.click()
            comment_box.send_keys(comment)

            driver.find_element(By.XPATH, "//button[@class = '_22S4OsoDdOqiM-hPTeOURa "
                                          "_2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts "
                                          "_3uJP0daPEH2plzVEYyTdaH ']").click()
            print(f"\n successfully commented on {comment_link}")

    except Exception:
        print(f"Comments were disabled for {comment_link}")

    time.sleep(3)
    logout_menu = driver.find_element(By.ID, "USER_DROPDOWN_ID")
    logout_menu.click()
    logout_btn = driver.find_element(By.XPATH, "//i[@class = '_2BQPq3iyS8t6kKtFmtkB30  icon icon-logout']")
    logout_btn.click()
    time.sleep(20)


# "pain" is the default text that will be used in the subreddit which do not allow posting w/o texts
def cross_posting(driver, username, password, from_sub_reddit, to_sub_reddit, text="pain"):
    """posts the top comments and meme cross sub-reddits"""

    try:

        driver.get(r"https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F")
        driver.find_element(By.CLASS_NAME, "AnimatedForm__textInput").send_keys(username, Keys.ENTER)
        driver.find_element(By.XPATH, "//*[@id='loginPassword']").send_keys(password, Keys.ENTER)

        time.sleep(5)

        data = recent_posts.get_recent_post(driver, from_sub_reddit)
        if len(data) == 2:
            meme_img = data[0]
            comm = data[1]
        else:
            meme_img = data
            comm = "XD"

        recent_posts.retrieve_img(meme_img)
        image_name = meme_img.split("/")[-1]
        path_to_image = os.getcwd() + "\\" + image_name

        driver.get("https://www.reddit.com/submit")

        # for the sub reddit selection
        driver.find_element(By.CLASS_NAME, "_1MHSX9NVr4C2QxH2dMcg4M").send_keys('r/' + to_sub_reddit)

        image_sec = driver.find_element(By.XPATH, "//*[@id='SHORTCUT_FOCUSABLE_DIV']/"
                                                  "div[2]/div/div/div/div[2]/div[3]"
                                                  "/div[1]/div[2]/div[3]/div[1]/div/button[2]")
        if image_sec.is_enabled():
            image_sec.click()
            upload = driver.find_element(By.XPATH, "//*[@id='SHORTCUT_FOCUSABLE_DIV']"
                                                   "/div[2]/div/div/div/div[2]/div[3]/"
                                                   "div[1]/div[2]/div[3]/div[2]/div[2]/div/div/input")
            upload.send_keys(path_to_image)

            time.sleep(3)

            # for title
            title_input = driver.find_element(By.XPATH, "//div[@class ='_3w_665DK_NH7yIsRMuZkqB']"
                                                        "/div[2]/div/div/textarea")
            title_input.click()
            title_input.send_keys(comm)

            time.sleep(3)

            done_btn = driver.find_element(By.XPATH, "//button[@class = '_18Bo5Wuo3tMV-RDB8-kh8Z "
                                                     "_2iuoyPiKHN3kfOoeIQalDT _10BQ7pjWbeYP63SAPNS8Ts "
                                                     "HNozj_dKjQZ59ZsfEegz8 ']")
            done_btn.click()

            time.sleep(3)

            driver.close()

        else:
            print(f"{to_sub_reddit} doesn't allow posting images")
            # for text of the content

    except Exception as e:
        print(f"Only approved users can post in {to_sub_reddit}", e)


def initial_farming(driver, username, password, to_sub_reddit):
    """replies to the top comments with memes and comments from other subreddits"""

    try:

        driver.get(r"https://www.reddit.com/login/?dest=https%3A%2F%2Fwww.reddit.com%2F")
        driver.find_element(By.CLASS_NAME, "AnimatedForm__textInput").send_keys(username, Keys.ENTER)
        driver.find_element(By.XPATH, "//*[@id='loginPassword']").send_keys(password, Keys.ENTER)

        time.sleep(5)

        driver.get(f"https://www.reddit.com/r/{to_sub_reddit}/top/?t=day")

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # selects top 5 posts to reply to
        comments_link = []
        for link in soup.find_all('a',
                                  attrs={'href': re.compile("^https://")}):
            # display the actual urls
            if "r/" + to_sub_reddit + "/comments" in link.get("href") and len(comments_link) < 5:
                temp = link.get("href").split()
                comments_link.append(temp)

        global n

        skip = sorted(random.sample(range(n), n - 6))
        df = pandas.read_csv("comments.csv", skiprows=skip)
        comm5 = df.values.tolist()  # list of 5 unique comments for posting
        count = 0
        link = random.choice(comments_link)
        try:
            driver.get(link[0])
            time.sleep(2)
            reply_btn = driver.find_element(By.XPATH, "(//button[@class = '_374Hkkigy4E4srsI2WktEd'])"
                                                      "[position()=3]")
            actions = ActionChains(driver)
            actions.move_to_element(reply_btn).perform()
            reply_btn.click()
            actions = ActionChains(driver)
            actions.move_to_element(reply_btn).perform()
            reply_box = driver.find_element(By.XPATH, "(//div[@class = 'notranslate "
                                                      "public-DraftEditor-content'])[position()=2]")

            reply_box.send_keys(comm5[count][0])
            count += 1
            driver.find_element(By.XPATH, "//div[@class='_1r4smTyOEZFO91uFIdWW6T "
                                          "JchsqHyN3thfSnN8dUM3 _2jhbZV6mVCM5Ma7Z376DW2 ']"
                                          "/div/div/div/div[3]/div/button").click()
            time.sleep(5)
        except Exception:
            print(f"The comments are disabled at {link[0]}", )

        else:
            print(f"Successfully replied to the top comment of {link[0]}")

        logout_menu = driver.find_element(By.ID, "USER_DROPDOWN_ID")
        logout_menu.click()
        logout_btn = driver.find_element(By.XPATH, "//i[@class = '_2BQPq3iyS8t6kKtFmtkB30  icon icon-logout']")
        logout_btn.click()
        time.sleep(5)

    except Exception:
        print(f"The account {username} has been used many times, "
              f"thus cannot further comment till a certain time has passed ")
        quit()


if __name__ == '__main__':

    # install_packages()

    print("Reddit Bot at your service :)")

    while True:
        print("""\n1) Scrape the inactive subreddits into inactive_mods_list.csv

2) Scrape the links for comment-section from the inactive communities

3) Scrape content for comments

4) Start with the karma farming (posting and commenting randomly)

5) Cross post the trending memes (pick the top memes and cross post them)

6) Initial Farming (replying to comments of popular subreddits) 

7) Exit""")

        print("\nNote: you can not stop farming until you close the program explicitly"
              "\nAlso, make sure to scrape data at least once before farming (i.e : opt 1 & 2)")

        option = input("\nYour option : ")

        if option == "1":
            print("\nThis might take some time")
            inactive_mods.scrape_data()

        elif option == "3":
            # add your subreddits in the following list
            driver = open_browser()
            for i in ["starterpacks", "wholesomememes", "AdviceAnimals", "Tinder",
                      "BikiniBottomTwitter", "HistoryMemes", "MemeEconomy", "ComedyCemetery",
                      "FellowKids", "bonehurtingjuice", "2meirl4meirl", "tumblr",
                      "terriblefacebookmemes", "meirl", "memes", "me_irl", "BlackPeopleTwitter",
                      "wheredidthesodago", "blunderyears", "talesfromthepizzaguy",
                      "mildlyinteresting", "CrappyDesign", "nottheonion", "natureisfuckinglit",
                      "HoldMyBeer", "Aww", "Facepalm", "CrappyDesign", "TrippinThroughTime",
                      "MildlyVandalized", "PerfectTiming", "WTF", "EarthPorn"]:

                get_comment_content(driver, i)
                print("Comments saved in comments.csv")

        elif option == "4":
            driver = open_browser()
            try:
                while True:
                    try:
                        while True:
                            # your accounts
                            credentials = [["Silent_Raspberry602", "asdfhjkl"], ["Icy_Efficiency5197", "asdfhjkl"],
                                           ['Henry321R', 'Reddit123!'], ['Robert321Lesher', 'Reddit123!'],
                                           ['Alexander321R', 'Reddit123!'], ['Mason321R', 'Reddit123!'],
                                           ['Michael321R', 'Reddit123!'], ['Ethan321R', 'Reddit123!'],
                                           ['Daniel321R', 'Reddit123!'], ['Jacob321R', 'Reddit123!'],
                                           ['Logan321R', 'Reddit123!'], ['Levi321R', 'Reddit123!'],
                                           ['Sebastian321R', 'Reddit123!'], ['Mateo321R', 'Reddit123!'],
                                           ['Owen321R', 'Reddit123!'], ['Theodore321R', 'Reddit123!'],
                                           ['Aiden321R', 'Reddit123!'], ['Samuel321R', 'Reddit123!'],
                                           ['Samuel321R', 'Reddit123!'], ['Joseph321R', 'Reddit123!'],
                                           ['Audrey321R', 'Reddit123!'], ['Audrey321R', 'Reddit123!'],
                                           ['John321R', 'Reddit123!'], ['Annette321R', 'Reddit123!'],
                                           ['David321R', 'Reddit123!'], ['Wyatt321R', 'Reddit123!'],
                                           ['Matthew321R', 'Reddit123!'], ['Antoinette321R', 'Reddit123!'],
                                           ['Luke321R', 'Reddit123!'], ['Luke321R', 'Reddit123!'],
                                           ['Asher321R', 'Reddit123!'], ['Carter321R', 'Reddit123!'],
                                           ['Julian321R', 'Reddit123!'], ['Grayson321R', 'Reddit123!'],
                                           ['Avril321R', 'Reddit123!'], ['Leo321R', 'Reddit123!'],
                                           ['Jayden321R', 'Reddit123!'], ['Gabriel321R', 'Reddit123!'],
                                           ['Isaac321RR', 'Reddit123!'], ['Lincoln321R', 'Reddit123!'],
                                           ['Brigitte321R', 'Reddit123!']]

                            credential = random.choice(credentials)

                            # randomly choosing a community from the scrapped data
                            community = random.choice(inactive_mods.use_list())

                            karma_farming(driver, credential[0], credential[1], community, "pain", "lol",
                                          "www.pain.com",
                                          "projection", "xD")
                            time.sleep(random.randint(180, 360))
                    except Exception as e:
                        print("There was a network error", e)
                        quit()

            except KeyboardInterrupt:
                pass

        elif option == "2":
            print("\nThis will take a while, please sit back.")
            comments.scrape_comments_link()

        elif option == "7":
            exit()

        elif option == "6":
            driver = open_browser()
            while True:
                try:
                    # your accounts
                    credentials = [["Silent_Raspberry602", "asdfhjkl"], ["Icy_Efficiency5197", "asdfhjkl"],
                                   ['Henry321R', 'Reddit123!'], ['Robert321Lesher', 'Reddit123!'],
                                   ['Alexander321R', 'Reddit123!'], ['Mason321R', 'Reddit123!'],
                                   ['Michael321R', 'Reddit123!'], ['Ethan321R', 'Reddit123!'],
                                   ['Daniel321R', 'Reddit123!'], ['Jacob321R', 'Reddit123!'],
                                   ['Logan321R', 'Reddit123!'], ['Levi321R', 'Reddit123!'],
                                   ['Sebastian321R', 'Reddit123!'], ['Mateo321R', 'Reddit123!'],
                                   ['Owen321R', 'Reddit123!'], ['Theodore321R', 'Reddit123!'],
                                   ['Aiden321R', 'Reddit123!'], ['Samuel321R', 'Reddit123!'],
                                   ['Samuel321R', 'Reddit123!'], ['Joseph321R', 'Reddit123!'],
                                   ['Audrey321R', 'Reddit123!'], ['Audrey321R', 'Reddit123!'],
                                   ['John321R', 'Reddit123!'], ['Annette321R', 'Reddit123!'],
                                   ['David321R', 'Reddit123!'], ['Wyatt321R', 'Reddit123!'],
                                   ['Matthew321R', 'Reddit123!'], ['Antoinette321R', 'Reddit123!'],
                                   ['Luke321R', 'Reddit123!'], ['Luke321R', 'Reddit123!'],
                                   ['Asher321R', 'Reddit123!'], ['Carter321R', 'Reddit123!'],
                                   ['Julian321R', 'Reddit123!'], ['Grayson321R', 'Reddit123!'],
                                   ['Avril321R', 'Reddit123!'], ['Leo321R', 'Reddit123!'],
                                   ['Jayden321R', 'Reddit123!'], ['Gabriel321R', 'Reddit123!'],
                                   ['Isaac321RR', 'Reddit123!'], ['Lincoln321R', 'Reddit123!'],
                                   ['Brigitte321R', 'Reddit123!']]

                    credential = random.choice(credentials)

                    pop_comms = ["starterpacks", "wholesomememes", "AdviceAnimals", "Tinder",
                                 "BikiniBottomTwitter", "HistoryMemes", "MemeEconomy", "ComedyCemetery",
                                 "FellowKids", "bonehurtingjuice", "2meirl4meirl", "tumblr",
                                 "terriblefacebookmemes", "meirl", "memes", "me_irl", "BlackPeopleTwitter",
                                 "wheredidthesodago", "blunderyears", "talesfromthepizzaguy",
                                 "mildlyinteresting", "CrappyDesign", "nottheonion", "natureisfuckinglit",
                                 "HoldMyBeer", "Aww", "Facepalm", "CrappyDesign", "TrippinThroughTime",
                                 "MildlyVandalized", "PerfectTiming", "WTF", "EarthPorn"]

                    from_comm = random.choice(pop_comms)
                    to_comm = random.choice(pop_comms)

                    initial_farming(driver, credential[0], credential[1], to_comm)

                except Exception:
                    print("There was a network error")
                    quit()

        elif option == '5':

            # your accounts
            credentials = [["Silent_Raspberry602", "asdfhjkl"], ["Icy_Efficiency5197", "asdfhjkl"],
                           ['Henry321R', 'Reddit123!'], ['Robert321Lesher', 'Reddit123!'],
                           ['Alexander321R', 'Reddit123!'], ['Mason321R', 'Reddit123!'],
                           ['Michael321R', 'Reddit123!'], ['Ethan321R', 'Reddit123!'],
                           ['Daniel321R', 'Reddit123!'], ['Jacob321R', 'Reddit123!'],
                           ['Logan321R', 'Reddit123!'], ['Levi321R', 'Reddit123!'],
                           ['Sebastian321R', 'Reddit123!'], ['Mateo321R', 'Reddit123!'],
                           ['Owen321R', 'Reddit123!'], ['Theodore321R', 'Reddit123!'],
                           ['Aiden321R', 'Reddit123!'], ['Samuel321R', 'Reddit123!'],
                           ['Samuel321R', 'Reddit123!'], ['Joseph321R', 'Reddit123!'],
                           ['Audrey321R', 'Reddit123!'], ['Audrey321R', 'Reddit123!'],
                           ['John321R', 'Reddit123!'], ['Annette321R', 'Reddit123!'],
                           ['David321R', 'Reddit123!'], ['Wyatt321R', 'Reddit123!'],
                           ['Matthew321R', 'Reddit123!'], ['Antoinette321R', 'Reddit123!'],
                           ['Luke321R', 'Reddit123!'], ['Luke321R', 'Reddit123!'],
                           ['Asher321R', 'Reddit123!'], ['Carter321R', 'Reddit123!'],
                           ['Julian321R', 'Reddit123!'], ['Grayson321R', 'Reddit123!'],
                           ['Avril321R', 'Reddit123!'], ['Leo321R', 'Reddit123!'],
                           ['Jayden321R', 'Reddit123!'], ['Gabriel321R', 'Reddit123!'],
                           ['Isaac321RR', 'Reddit123!'], ['Lincoln321R', 'Reddit123!'],
                           ['Brigitte321R', 'Reddit123!']]

            credential = random.choice(credentials)

            sub_reddits = input("Enter the sub_reddits from where you want to scrape and post, separated by commas: ")
            sub_reddits = sub_reddits.split(',')

            cross_posting(open_browser(), credential[0], credential[1], sub_reddits[0], sub_reddits[1])
        else:
            print("Please enter a valid option")
