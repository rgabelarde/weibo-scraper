# Import required packages
# Basic Python Packages
import asyncio
import os
import re
import sys
import time

import lxml
import pandas as pd
import requests
# External Packages
from bs4 import BeautifulSoup
from selenium import webdriver  # for webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scrape_pics(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('../webdrivers/chromedriver',
                              options=chrome_options)

    driver.get(url)

    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since weibo dynamically loads them).
    last_height = driver.execute_script(
        'return document.documentElement.scrollHeight')

    # scroll to end of page 5 times
    for i in range(5):
        # Scroll down 'til 'next load'.
        driver.execute_script(
            'window.scrollTo(0, document.documentElement.scrollHeight);')

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script(
            'return document.documentElement.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

    # One last scroll just in case.
    driver.execute_script(
        'window.scrollTo(0, document.documentElement.scrollHeight);')

    # Wait to load everything thus far.
    time.sleep(3)

    #Selenium hands the page source to Beautiful Soup
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    soup_post_info = soup.find_all('div', {'class': 'img'})
    soup_author_info = soup.find_all('p', {'class': 'name'})

    post_img_urls, post_captions, author_urls, author_usernames = ([], ) * 4

    # For scraping of posts info
    try:
        post_img_urls = [
            "https://" + res.img['src'][2:] for res in soup_post_info
        ]
        post_captions = [
            res.find(class_='img_info').get_text() for res in soup_post_info
        ]

    except:
        print("Error scraping posts info")

    # For scraping of authors info
    try:
        author_urls = [
            "https://" + res.a['href'][2:] for res in soup_author_info
        ]
        author_usernames = [res.a['title'] for res in soup_author_info]

    except:
        print("Error scraping authors info")

    df = pd.DataFrame({
        'post_caption': post_captions,
        'post_img_url': post_img_urls,
        'author_username': author_usernames,
        'author_url': author_urls
    })

    df.to_excel(r'weibo_keyword_search_output.xlsx', index=False)


'''
def scrape_users(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('../webdrivers/chromedriver',
                              options=chrome_options)

    driver.get(url)
    
    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since weibo dynamically loads them).
    last_height = driver.execute_script(
        'return document.documentElement.scrollHeight')

    # scroll to end of page 5 times
    for i in range(5):
        # Scroll down 'til 'next load'.
        driver.execute_script(
            'window.scrollTo(0, document.documentElement.scrollHeight);')

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script(
            'return document.documentElement.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

    # One last scroll just in case.

    driver.execute_script(
        'window.scrollTo(0, document.documentElement.scrollHeight);')

    # Wait to load everything thus far.
    time.sleep(3)

    #Selenium hands the page source to Beautiful Soup
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    soup_profile_info = soup.find_all(
        'div', {'class': 'card card-user-b s-pg16 s-brt1'})

    # user_url, user_username, user_sex, user_country, user_role, num_of_friends, num_of_fans, user_wbcount, user_bio, user_tags = ([], ) * 10

    if soup_profile_info is not None:
        for soup_profile in soup_profile_info:
            # Set default values in case nothing is returned
            user = {
                'username': "",
                'url': "",
                # 'sex': "",
                'country': "",
                'role': "",
                'num_of_friends': 0,
                'num_of_fans': 0,
                'user_wbcount': 0,
                'user_bio': '',
                'user_tags': [],
            }
            user['url'] = soup_profile.find(class_='avator').a['href']

            soup_info = soup_profile.find(class_='info')
            user['username'] = soup_info.find(
                class_='name').get_text()
            # user['sex'] = 'male' if (soup_info.i == 'icon-sex icon-sex icon-sex-male') else 'female'

            soup_paras = soup_info.find_all('p')
            user['country'] = soup_paras.get_text().replace(" ", ", ").strip()
            user['url'] = soup_info.find(class_='avator').a['href']
            user['url'] = soup_info.find(class_='avator').a['href']
            user['url'] = soup_info.find(class_='avator').a['href']

    df = pd.DataFrame({
        'post_caption': post_captions,
        'post_img_url': post_img_urls,
        'author_username': author_usernames,
        'author_url': author_urls
    })

    df.to_excel(r'weibo_keyword_search_output.xlsx', index=False)
'''


def scrape_posts_urls(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('../webdrivers/chromedriver',
                              options=chrome_options)

    driver.get(url)

    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since weibo dynamically loads them).
    driver.execute_script(
        'window.scrollTo(0, document.documentElement.scrollHeight);')

    # Wait to load everything thus far.
    time.sleep(2)

    #Selenium hands the page source to Beautiful Soup
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    soup_posts = soup.find_all('p', {'class': 'from'})

    # For scraping of posts url info
    try:
        post_urls = ["https://" + link.a['href'][2:] for link in soup_posts]
        return post_urls

    except:
        print("Error scraping posts info")
        return []


def scrape_post(url):
    RES = {
        'url': url,
        'post_content': "",
        'posted_timedate': "",
        'hashtags': "",
        'author_username': "",
        'author_url': "",
        'media_url': "",
    }

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('../webdrivers/chromedriver',
                              options=chrome_options)

    driver.get(url)
    delay = 20  # seconds

    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since weibo dynamically loads them).
    driver.execute_script(
        'window.scrollTo(0, document.documentElement.scrollHeight);')

    try:
        WebDriverWait(driver, delay, poll_frequency=1).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "WB_feed_detail clearfix")))
    except TimeoutException as e:
        print("Wait Timed out")
        print(e)

    # Wait to load everything thus far
    # time.sleep(10)
    # driver.implicitly_wait(10)

    #Selenium hands the page source to Beautiful Soup
    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    post = RES
    try:
        soup_author = soup.find(class_='W_face_radius')
        post['author_username'] = soup_author['title']
        post['author_url'] = "https://" + soup_author['href'][2:]
        post['posted_timedate'] = soup.find(class_='S_txt2').a['title']

        soup_post = soup.find(class_='WB_text W_f14')
        post_content = soup_post.get_text()
        post['post_content'] = re.sub(r'#.+?#', '',
                                      post_content).strip()  # removes hashtags
        try:
            post['hashtags'] = ", ".join([
                hashtag.get_text().strip("#")
                for hashtag in soup_post.find_all('a', {'class': 'a_topic'})
            ])

            soup_media = soup_post.find_all('a')[-1]
            post['media_url'] = soup_media['href']
        except:
            pass

    except:
        print("error")
    # print(RES)
    return RES


if __name__ == '__main__':
    url = sys.argv[1]
    if url.find('pic?q=') != -1:
        scrape_pics(url)
    # elif url.find('user?q=') != -1:
    #     scrape_users(url)
    elif (url.find('/weibo/') and url.find('?topnav=1')
          ) or url.find('weibo?q=') != -1 or url.find('hot?q=') != -1:
        url_lst = scrape_posts_urls(url)
        data = pd.DataFrame(map(scrape_post, url_lst))
        pd.DataFrame(data).to_excel(r'weibo_keyword_posts_output.xlsx',
                                    index=False)
    else:
        print('wrong')
