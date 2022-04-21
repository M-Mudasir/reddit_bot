import re
from bs4 import BeautifulSoup
import pandas as pd


def get_comment_content(driver, sub_reddit):
    """ saves the newly scrapped top comments into the comments.csv file """

    driver.get(f"https://www.reddit.com/r/{sub_reddit}/top/?t=day")

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    comments_link = []
    for link in soup.find_all('a',
                              attrs={'href': re.compile("^https://")}):
        # display the actual urls
        if "r/" + sub_reddit + "/comments" in link.get("href") and len(comments_link) < 8:
            temp = link.get("href").split()
            comments_link.append(temp)

    comm = []
    for link in comments_link:
        driver.get(link[0])
        soup_ = BeautifulSoup(driver.page_source, 'html.parser')
        all_comments = soup_.find_all("p", class_="_1qeIAgB0cPwnLhDF9XSiJM")
        for comment in all_comments:
            if ("Thanks for your submission" not in comment.get_text()) and ("bot" not in comment.get_text())\
                    and ("Remember to remove all names and usernames from posts" not in comment.get_text()):
                comm.append(comment.get_text())

    df = pd.DataFrame(comm)
    df.to_csv("comments.csv", index=False)

