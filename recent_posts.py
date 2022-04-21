import re
from bs4 import BeautifulSoup
import requests
import shutil  # to save it locally


def get_recent_post(driver, sub_reddit):
    """ returns the link of top most recent meme and the comment on it """

    driver.get(f"https://www.reddit.com/r/{sub_reddit}/top/?t=day")

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    comments_link = []
    for link in soup.find_all('a',
                              attrs={'href': re.compile("^https://")}):

        # display the actual urls
        if "r/" + sub_reddit + "/comments" in link.get("href"):
            comments_link.append(str(link.get("href")))

    comments_link = comments_link[:8]

    img = []
    count = 0
    comm = []
    for link in comments_link:
        if count == 0:
            driver.get(link)
            soup_ = BeautifulSoup(driver.page_source, 'html.parser')
            all_divs = soup_.find_all('a',
                                      attrs={'href': re.compile("^https://")})
            for div in all_divs:
                if len(img) < 1:
                    if '.jpg' in div.get("href"):
                        img.append(div.get("href"))
                        count += 1
                elif len == 1:
                    break

            all_comments = soup_.find_all("p", class_="_1qeIAgB0cPwnLhDF9XSiJM")
            for comment in all_comments:
                comm.append(comment.get_text())
        else:
            break

    try:
        return img[0], comm[6]

    except IndexError:
        return img[0]


def retrieve_img(url):

    filename = url.split("/")[-1]

    # Open the url image, set stream to True, this will return the stream content.
    r = requests.get(url, stream=True)

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image Couldn\'t be retreived')
