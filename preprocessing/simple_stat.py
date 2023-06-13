# -*-coding:utf-8-*-
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import json

# Thread 사용

def open_window(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--blink-settings=imagesEnabled=false')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    return driver


def get_soup(d):
    html = d.page_source
    s = BeautifulSoup(html, 'html.parser')  # s = soup
    return s


def get_title(s):
    title = s.select_one('.media_end_head_headline').text
    return title


def get_article_date(s):
    date = s.select_one('.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME').text
    return date


def get_n_reply(s):
    try:
        n_reply = s.select_one('.u_cbox_count').text
    except:
        n_reply = s.select_one('#comment_count').text
    return n_reply


if __name__ == "__main__":
    # date_start = datetime.datetime(2021, 7, 1)
    date_now = datetime.datetime(2021, 7, 1)
    # date_end = datetime.datetime(2022, 7, 31)
    # print(date_end-date_start)
    df = pd.DataFrame(columns={'title', 'n_reply', 'date', 'url'})
    url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query=%22%EC%97%90%EB%84%88%EC%A7%80+%EC%A0%84%ED%99%98%22&oquery=%EC%97%90%EB%84%88%EC%A7%80+%EC%A0%84%ED%99%98&tqi=hzYKjwprvmZss6%2FMzQKssssst6G-274078&nso=so%3Ar%2Cp%3Afrom20210701to20210701&de=2021.07.01&ds=2021.07.01&mynews=0&office_section_code=0&office_type=0&pd=3&photo=0&sort=2'
    for i in range(396):        #date_end - date_start
        d = open_window(url)
        while True:
            elem = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "news_area")))
            ls_news = d.find_elements(By.CLASS_NAME, 'news_area')
            for i in ls_news:
                if '네이버뉴스' == i.find_element(By.CLASS_NAME, 'info_group').text[-5:]:
                    btn_naver = i.find_elements(By.TAG_NAME, 'a')[4]
                    naver_url = btn_naver.get_attribute('href')
                    if 'entertain' in naver_url:
                        continue
                    if 'sports' in naver_url:
                        continue
                    d.switch_to.new_window('window')
                    d.get(naver_url)
                else:
                    continue
                try:
                    elem = WebDriverWait(d, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "u_cbox_count")))
                    s = get_soup(d)
                    if int(get_n_reply(s)) < 1:
                        continue
                    df.loc[len(df)] = [get_title(s), get_article_date(s), get_n_reply(s), naver_url]
                except:
                    pass
                finally:
                    d.close()
                    d.switch_to.window(d.window_handles[0])
            btn_next = d.find_element(By.CLASS_NAME, 'btn_next')
            next_avail = btn_next.get_attribute('aria-disabled')
            if next_avail == 'true':
                break
            btn_next.click()
            print(len(df))
            time.sleep(1)
        d.quit()
        day_after = date_now+datetime.timedelta(days=1)
        url = url.replace(date_now.strftime('%Y.%m.%d'), day_after.strftime('%Y.%m.%d'))
        url = url.replace(date_now.strftime('%Y%m%d'), day_after.strftime('%Y%m%d'))
        date_now = date_now + datetime.timedelta(days=1)
    df.to_csv('simple_stat.csv', encoding='UTF-8-sig')
    print('utf-8-sig')