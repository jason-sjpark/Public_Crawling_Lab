# -*-coding:utf-8-*-
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options
import subprocess
import json
import os
from multiprocessing import Process
import multiprocessing
import threading
import requests
import json
import re
import os



# Thread 사용

def open_window(url):
    # try:
    #     subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 '
    #                      r'--user-data-dir="C:\chrometemp"')  # Open the debugger chrome
    #
    # except FileNotFoundError:
    #     subprocess.Popen(
    #         r'C:\Users\binsu\AppData\Local\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 '
    #         r'--user-data-dir="C:\chrometemp"')

    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    options.add_argument('user-agent=' + user_agent)
    options.add_argument('--disable-extensions')
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--blink-settings=imagesEnabled=false')
    # options.add_argument('--incognito')
    # options.add_argument('--disable-application-cache')
    # options.add_argument('--test-type')
    # options.add_argument('--disk-cache-size=1')
    # options.add_argument('--media-cache-size=1')
    # options.add_argument('--disk-cache-dir=/dev/null')g
    # options.add_argument('--js-flags=--expose-gc')
    # options.add_argument('--enable-precise-memory-info')
    # options.add_argument('--disable-default-apps')
    # options.add_argument('--disable-dev-shm-usage')
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

    # 안될때 대비
    # s = Service('chromedriver.exe')
    # driver = webdriver.Chrome(service=s, options=options)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    # driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})
    # wait 3가지
    # time.sleep(10)
    # driver.implicitly_wait(10)
    return driver


def get_soup(d):
    # without selenium, only soup
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.141 Whale/3.15.136.29 Safari/537.36"}
    # url = 'https://n.news.naver.com/mnews/article/016/0002012681?sid=100'
    # response = requests.get(url, headers=headers)
    # html = response.text
    html = d.page_source
    s = BeautifulSoup(html, 'html.parser')  # s = soup
    return s


def get_title(s):
    title = s.select_one('.media_end_head_headline').text
    # 특수 문자 제거
    # pattern1 = '<[^>]*>'
    # title = re.sub(pattern=pattern1, repl='', string=str(title))
    return title


def get_article_date(s):
    date = s.select_one('.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME').text
    return date


def get_press(s):
    press = s.select('.u_cra_v1')[1].text
    return press


def get_reporter(s):
    try:
        return s.select_one('.media_end_head_journalist_name').text
    except:
        return ''


def get_article(s):
    article = s.select_one('#dic_area').text.replace('\n', '')
    return article


def get_n_emotion(s):
    try:
        n_emotion = s.select_one('.u_likeit_text._count.num').text
    except:
        n_emotion = s.select_one('.u_likeit_text._count').text
    if n_emotion == '추천':
        return ''
    elif n_emotion == '공감':
        return ''
    else:
        return n_emotion


def get_n_reply(s):
    n_reply = s.select_one('.u_cbox_count').text
    return n_reply


def get_n_each_emotion(s):
    ls_each_emotion = s.select('.u_likeit_list_count._count')
    n_each_emotion = dict()
    n_each_emotion['좋아요'] = ls_each_emotion[0].text
    n_each_emotion['훈훈해요'] = ls_each_emotion[1].text
    n_each_emotion['슬퍼요'] = ls_each_emotion[2].text
    n_each_emotion['화나요'] = ls_each_emotion[3].text
    n_each_emotion['후속기사원해요'] = ls_each_emotion[4].text
    return n_each_emotion


def get_ratios(s):
    dict_gender = dict()
    dict_ages = dict()
    ratios = s.select('.u_cbox_chart_progress_in')
    if ratios == []:
        return dict_gender, dict_ages
    dict_gender['남자'] = ratios[0].attrs['style'][7:-1]
    dict_gender['여자'] = ratios[1].attrs['style'][7:-1]
    dict_ages['10대'] = ratios[2].attrs['style'][7:-1]
    dict_ages['20대'] = ratios[3].attrs['style'][7:-1]
    dict_ages['30대'] = ratios[4].attrs['style'][7:-1]
    dict_ages['40대'] = ratios[5].attrs['style'][7:-1]
    dict_ages['50대'] = ratios[6].attrs['style'][7:-1]
    dict_ages['60대 이상'] = ratios[7].attrs['style'][7:-1]
    return dict_gender, dict_ages


def get_list_reply(s):
    list_reply = s.select_one('.u_cbox_list').contents
    return list_reply


def get_reply_id(reply):
    reply_id = reply.attrs['class'][1].split('_')[-1]
    return reply_id


def get_user_id(reply):
    user_id = reply.attrs['class'][2].split('_')[-1]
    return user_id


def get_nickname(reply):
    nickname = reply.select_one('.u_cbox_nick').text
    return nickname


def get_hierarchy_level(reply):
    hierarchy_level = reply.attrs['data-info'].split('replyLevel:')[1][0]
    return hierarchy_level


def get_reply_date(reply):
    reply_date = reply.select_one('.u_cbox_date').text
    return reply_date


def get_reply_text(reply):
    try:
        return reply.select_one('.u_cbox_contents').text
    except:
        return ''


def get_n_good(reply):
    try:
        return reply.select_one('.u_cbox_cnt_recomm').text
    except:
        return '0'


def get_n_bad(reply):
    try:
        return reply.select_one('.u_cbox_cnt_unrecomm').text
    except:
        return '0'


def get_n_son_reply(reply):
    try:
        return reply.select_one('.u_cbox_reply_cnt').text
    except:
        return '0'


def get_parents_user_id(son_reply):
    parents_user_id = son_reply.attrs['data-info'].split('parentCommentNo:\'')[1].split(',')[0][:-1]
    return parents_user_id


def get_start_date(s):
    return s.select_one('.u_cbox_userinfo_meta_date').text[:-5]


def get_sum_reply(s):
    return s.select('.u_cbox_currentstats_number')[0].text


def get_sum_son_reply(s):
    return s.select('.u_cbox_currentstats_number')[1].text


def get_sum_emotion(s):
    return s.select('.u_cbox_currentstats_number')[2].text


def get_recent_n_reply(s):
    return s.select('.u_cbox_lateststats_dataitem')[0].text[2:]


def get_recent_n_deleted(s):
    return s.select('.u_cbox_lateststats_dataitem')[1].text[2:]


def get_recent_n_emotion(s):
    return s.select('.u_cbox_lateststats_dataitem')[2].text[4:]


def get_recent_rate_emotion(s):
    return s.select('.u_cbox_lateststats_progressnum')[0].text + '%'


def get_recent_rate_self_delete(s):
    return s.select('.u_cbox_lateststats_progressnum')[1].text + '%'


def get_url_history(reply):
    return reply.select_one('.u_cbox_orgsource').contents[0].attrs['href']


def get_title_history(reply):
    return reply.select_one('.u_cbox_orgsource_header').text


def get_press_history(reply):
    return reply.select_one('.u_cbox_orgsource_name').text


def get_n_reply_history(reply):
    return reply.select_one('.u_cbox_orgsource_count').text[2:]


def get_user_nickname(s):
    return s.select_one('.u_cbox_userinfo_meta_nickname').text


def view_all_son_reply(d):
    ls_reply = d.find_elements(By.CLASS_NAME, 'u_cbox_btn_reply')
    for btn_son_reply in ls_reply:
        if btn_son_reply.text.split('\n')[1] != '0':
            y = str(btn_son_reply.location['y'] - 50)
            d.execute_script("window.scrollTo(0, " + y + ")")
            try:
                btn_son_reply.click()
            except:
                continue
    time.sleep(1)  # optimal은 아님
    # 더보기 및 자식 댓글들 펼치기 완료시, 페이지 파싱
    s = get_soup(d)
    return s


def view_all_reply(d):
    try:
        d.find_element(By.CLASS_NAME, 'u_cbox_btn_view_comment').click()
        elem = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'u_cbox_btn_more')))
        # 더보기 버튼 찾기 위한 soup 설정
        while True:  # 더보기 버튼이 있는동안
            d.find_element(By.CLASS_NAME, 'u_cbox_btn_more').click()
    except:
        s = get_soup(d)
        ls_btn_parents = d.find_elements(By.CLASS_NAME, 'u_cbox_btn_totalcomment')
        return s, ls_btn_parents


def get_dic_son_reply(reply):
    ls_dic_son_reply = list()
    ls_son_reply = reply.select_one('.u_cbox_list').contents
    for son_reply in ls_son_reply:
        try:
            son_reply_text = get_reply_text(son_reply)
        except:
            continue
        ls_dic_son_reply.append(
            {'parents_user_id': get_parents_user_id(son_reply), 'son_reply_id': get_reply_id(son_reply),
             'son_user_id': get_user_id(son_reply), 'son_nickname': get_nickname(son_reply),
             'son_reply_date': get_reply_date(son_reply), 'son_reply_text': son_reply_text,
             'son_n_good': get_n_good(son_reply), 'son_n_bad': get_n_bad(son_reply),
             'hierarchy_level': get_hierarchy_level(son_reply)})
    return ls_dic_son_reply


def get_dic_reply_history(d, proc_id, url):
    oid = url.split("_news")[1].split(",")[0]  # 001
    aid = url.split("_news")[1].split(',')[1]
    commentNo = url.split("comment_")[1].split("_news")[0]  # 0013014070
    header = {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "referer": url,
    }
    c_url = "https://apis.naver.com/commentBox/cbox/web_naver_user_info_jsonp.json?" \
            "ticket=news&pool=cbox5&lang=ko&country=KR&objectId=news" + oid + "%2C" + aid + "&categoryId=&pageSize=20" \
            "&indexSize=10&groupId=&listType=user&pageType=more&commentNo=" + commentNo + \
            "&includeAllStatus=true"
    r = requests.get(c_url, headers=header)
    cont = BeautifulSoup(r.content, "html.parser")
    cont = str(cont)
    ls_dic_reply_history = list()
    ls_url = cont.split('"objectUrl":"')
    for i in range(len(ls_url)-1):
        i = i+1
        url = ls_url[i].split('"')[0]
        text = ls_url[i].split('"contents":"')[1].split('"')[0]
        try:
            date = ls_url[i].split('"modTime":"')[1].split('+')[0].replace("T", ' ')
        except:
            date = ''
        finally:
            try:
                good = ls_url[i].split('"sympathyCount":')[1].split(',')[0]
                bad = ls_url[i].split('"antipathyCount":')[1].split(',')[0]
                press = ls_url[i].split('"publisherName":"')[1].split('"')[0].replace('"', '')
                title = ls_url[i].split('"title":"')[1].split('"')[0]
                n_reply = ls_url[i].split('"commentCount":')[1].split(',')[0]
            except:
                good = 'null'
                bad = 'null'
                press = 'null'
                title = 'null'
                n_reply = 'null'
            ls_dic_reply_history.append(
                {'text': text, 'date': date,
                 'good': good, 'bad': bad,
                 'url': url, 'title': title, 'press': press,
                 'n_reply': n_reply})
    nextid = cont.split('"next":"')[1].split('"')[0]
    endid = cont.split('"end":"')[1].split('"')[0]
    if nextid == endid:
        return ls_dic_reply_history
    while(len(ls_dic_reply_history) < 5000):  # 더보기 버튼이 있는동안
        c_url = "https://apis.naver.com/commentBox/cbox/web_naver_list_per_user_jsonp.json?" \
                "ticket=news&pool=cbox5" \
                "&lang=ko&country=KR" \
                "&objectId=news" + oid + "%2C" + aid + "&categoryId=&pageSize=20&indexSize=10&groupId=" \
                "&listType=user&pageType=more&page=2&sort=NEW" \
                "" \
                "&moreParam.next=" + nextid + "&commentNo=" + commentNo + \
                "&includeAllStatus=true"
        try:
            r = requests.get(c_url, headers=header)
        except:
            break
        cont = BeautifulSoup(r.content, "html.parser")
        cont = str(cont)
        ls_url = cont.split('"objectUrl":"')
        for i in range(len(ls_url) - 1):
            i = i + 1
            url = ls_url[i].split('"')[0]
            text = ls_url[i].split('"contents":"')[1].split('"')[0]
            try:
                date = ls_url[i].split('"modTime":"')[1].split('+')[0].replace("T", ' ')
            except:
                date = ''
            finally:
                try:
                    good = ls_url[i].split('"sympathyCount":')[1].split(',')[0]
                    bad = ls_url[i].split('"antipathyCount":')[1].split(',')[0]
                    press = ls_url[i].split('"publisherName":"')[1].split('"')[0].replace('"', '')
                    title = ls_url[i].split('"title":"')[1].split('"')[0]
                    n_reply = ls_url[i].split('"commentCount":')[1].split(',')[0]
                except:
                    good = 'null'
                    bad = 'null'
                    press = 'null'
                    title = 'null'
                    n_reply = 'null'
                ls_dic_reply_history.append(
                    {'text': text, 'date': date,
                     'good': good, 'bad': bad,
                     'url': url, 'title': title, 'press': press,
                     'n_reply': n_reply})
        try:
            nextid = cont.split('"next":"')[1].split('"')[0]
            endid = cont.split('"end":"')[1].split('"')[0]
            if nextid == endid:
                break
        except:
            break
    return ls_dic_reply_history


def get_dic_history(d, btn_history, user_id, nickname, proc_id):
    y = str(btn_history.location['y'] - 50)
    d.execute_script("window.scrollTo(0, " + y + ")")
    btn_history.click()
    elem = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "u_cbox_lateststats")))
    curr_url = d.current_url
    s = get_soup(d)
    dic_history = {'user_id': user_id, 'nickname': nickname,
                           'user_real_nickname': get_user_nickname(s),
                           'start_date': get_start_date(s), 'sum_reply': get_sum_reply(s),
                           'sum_son_reply': get_sum_son_reply(s), 'sum_emotion': get_sum_emotion(s),
                           'recent_n_reply': get_recent_n_reply(s), 'recent_n_deleted': get_recent_n_deleted(s),
                           'recent_n_emotion': get_recent_n_emotion(s),
                           'recent_rate_emotion': get_recent_rate_emotion(s),
                           'recent_rate_self_delete': get_recent_rate_self_delete(s),
                           'dic_reply_history': get_dic_reply_history(d, proc_id, curr_url)}
    d.find_element(By.CLASS_NAME, 'u_cbox_userpage_closebtn').click()
    return dic_history


def get_dic_reply(d, proc_id):
    global ls_user_id
    s, ls_btn_parents = view_all_reply(d)  # ls_btn_parents = 유효한 댓글 리스트
    ls_dic_reply = list()
    list_reply = get_list_reply(s)  # list_reply = 모든 댓글 리스트
    n = -1
    for reply in list_reply:
        user_id = get_user_id(reply)
        nickname = get_nickname(reply)
        if user_id == 'null':  # 작성자에 의해 삭제된 댓글입니다. 일 경우 댓글 무시
            continue
        n += 1  # len(df_reply)보다 이 방법이 더 빠름
        if user_id in ls_user_id:
            ls_dic_reply.append({'reply_id': get_reply_id(reply), 'user_id': user_id, 'nickname': nickname,
                                 'reply_date': get_reply_date(reply), 'reply_text': get_reply_text(reply),
                                 'n_good': get_n_good(reply), 'n_bad': get_n_bad(reply),
                                 'n_son_reply': get_n_son_reply(reply),
                                 'hierarchy_level': get_hierarchy_level(reply), 'dic_son_reply': '',
                                 'dic_history': ''})
        else:
            ls_user_id.append(user_id)
            ls_dic_reply.append({'reply_id': get_reply_id(reply), 'user_id': user_id, 'nickname': nickname,
                                 'reply_date': get_reply_date(reply), 'reply_text': get_reply_text(reply),
                                 'n_good': get_n_good(reply), 'n_bad': get_n_bad(reply),
                                 'n_son_reply': get_n_son_reply(reply),
                                 'hierarchy_level': get_hierarchy_level(reply), 'dic_son_reply': '',
                                 'dic_history': get_dic_history(d, ls_btn_parents[n], user_id, nickname, proc_id)})

    # 자식 댓글은 나중에 추가
    s = view_all_son_reply(d)
    list_reply = get_list_reply(s)  # 자식들도 있는지 확인
    n = 0
    for reply in list_reply:
        try:
            n_son_reply = get_n_son_reply(reply)
            if n_son_reply != '0':  # 답글 있을때
                ls_dic_reply[n]['dic_son_reply'] = get_dic_son_reply(reply)
        except:  # 삭제된 댓글일 때
            continue
        n += 1
    return ls_dic_reply


def crawl(ls_idx, df_simple_stat, proc_id):
    for idx in ls_idx:
        if df_simple_stat.loc[idx]['n_reply'] >= 100:
            start_time = datetime.datetime.now()
            url = df_simple_stat.loc[idx]['url']
            d = open_window(url)
            elem = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CLASS_NAME, "u_cbox_in_view_comment")))
            s = get_soup(d)
            dic_article = dict()
            dic_article['title'] = get_title(s)
            dic_article['article_date'] = get_article_date(s)  # tag = soup.select('span')[27]['data-date-time']   //속성으로 요소 찾기
            dic_article['press'] = get_press(s)
            dic_article['reporter'] = get_reporter(s)
            dic_article['article'] = get_article(s)
            dic_article['n_emotion'] = get_n_emotion(s)
            dic_article['n_reply'] = get_n_reply(s)
            dic_article['n_each_emotion'] = get_n_each_emotion(s)
            ls_reply_type = s.select('.u_cbox_info_txt')
            dic_article['n_now_reply'] = ls_reply_type[0].text
            dic_article['n_deleted_reply'] = ls_reply_type[1].text
            dic_article['n_restricted_reply'] = ls_reply_type[2].text
            dic_article['url'] = url
            dic_article['gender_ratio'], dic_article['age_ratio'] = get_ratios(s)  # ratio 없을 때 예외 처리 필요
            dic_article['dic_reply'] = get_dic_reply(d, proc_id)
            # filename = dic_article['title'] + ".json"
            # filename = "".join(i for i in filename if i not in "\/:*?<>|")
            # filename = filename.replace('"', '')
            with open(str((idx*3)+1) + ".json", "w", encoding='UTF-8-sig') as json_file:
                json.dump(dic_article, json_file, indent=2, ensure_ascii=False)
            print(datetime.datetime.now() - start_time, str((idx*3)+1) + ".json")
            d.quit()
ls_user_id = []
if __name__ == "__main__":
    # #MultiProcessing
    n_proc = 8
    ls_idx = [[] for i in range(n_proc)]
    df_simple_stat = pd.read_csv('file2.csv')
    dir_files = os.listdir(os.getcwd())
    already_files = []
    for file in dir_files:
        if file[-4:] == 'json':
            already_files.append(int(file[:-5]))
    ls_file2 = list()           ##아직 수집되지 않은 파일의 df_simple_stat 상의 index 리스트
    for i in range(len(df_simple_stat)):
        if (i*3)+1 not in already_files:
            ls_file2.append(i)
    for i in ls_file2:
        if i % n_proc == 0:
            ls_idx[0].append(i)
        elif i % n_proc == 1:
            ls_idx[1].append(i)
        elif i % n_proc == 2:
            ls_idx[2].append(i)
        elif i % n_proc == 3:
            ls_idx[3].append(i)
        elif i % n_proc == 4:
            ls_idx[4].append(i)
        elif i % n_proc == 5:
            ls_idx[5].append(i)
        elif i % n_proc == 6:
            ls_idx[6].append(i)
        else:
            ls_idx[7].append(i)
    procs = []
    for i in range(n_proc):
        p = multiprocessing.Process(target=crawl, args=(ls_idx[i],df_simple_stat, i))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()  # 프로세스가 모두 종료될 때까지 대기