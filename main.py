# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import time

driver = webdriver.Firefox(capabilities=None, executable_path='/usr/local/bin/geckodriver')
link_list = []
news_title_list = []
real_news_link = []
date = ""
news_dic = dict()

def login():
    driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https://blog.naver.com/shn413')
    id = ""
    pw = ""
    copy_input_xpath('//*[@id="id"]', id)
    time.sleep(1)
    copy_input_xpath('//*[@id="pw"]', pw)
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()

def copy_input_xpath(xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    time.sleep(2)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()

def copy_input_css(css, input):
    pyperclip.copy(input)
    ele = driver.find_element_by_css_selector(css)
    ActionChains(driver).move_to_element(ele).click().perform()
    time.sleep(2)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()

def crawl_naver_main_news():
    base_url = "https://land.naver.com"
    url_for_date = "https://land.naver.com/news/headline.nhn"  # 주요뉴스

    response = requests.get(url_for_date)
    # if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    date_list = []
    date_list = soup.select("span.num")
    for elm in date_list:
        global date
        date += elm.text
    url = url_for_date + "?bss_ymd=" + date # 네이버 날짜별 주요뉴스 메인화면
    # print(url)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    main_news_list = soup.select("ul.headline_list > li > dl > dt:nth-of-type(2) > a")  # 이미지가 없을경우 고려 안되어 있으
    print("news count: "+str(len(main_news_list)))
    for link in main_news_list:
        link_list.append(base_url + link['href'])
        news_title_list.append(link.text)


def get_real_press():     # 뉴스 제목으로 실제 언론사 url 가져오기
    news_query = 'https://search.naver.com/search.naver?where=news&query='
    for i, title in enumerate(news_title_list):
        time.sleep(1)
        print("%d %s" % (i+1, title))
        driver.get(news_query+title)
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a._sp_each_title"))
            )
        except Exception as err:
            # news_title_list.remove(title) -
            print("not found", err)
            continue
        else:
            element.click()
            time.sleep(4)
            driver.switch_to.window(driver.window_handles[1])
            new_url = driver.current_url
            real_news_link.append(new_url)
            print(new_url)
            driver.close();
            driver.switch_to.window(driver.window_handles[0])

def make_dict():
    print("title cnt" + str(len(news_title_list)) + " link cnt: "+str(len(real_news_link)))
    for title, link in zip(news_title_list, real_news_link):
        news_dic[title] = link
        # print(title, link)

def close_popup():
    time.sleep(2)
    driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="mainFrame"]'))
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div#post-admin a.col._checkBlock._rosRestrict"))
    )
    element.click() # 글쓰기 버튼 클릭
    time.sleep(2)
    try:
        driver.find_element_by_css_selector('button.se-popup-button-cancel').is_displayed()
    except Exception as err:
        print("no popup", err)
    else:
        driver.find_element_by_css_selector('button.se-popup-button-cancel').click()
    time.sleep(1)
    try:
        driver.find_element_by_css_selector('button.se-help-panel-close-button').is_displayed()
    except Exception as err:
        print("no article popup", err)
    else:
        driver.find_element_by_css_selector('button.se-help-panel-close-button').click()
    time.sleep(2)
    # driver.switch_to.frame(driver.find_element_by_id('blog-editor'))


def write_blog():
    global date
    date = date[:4]+'.'+date[4:6]+'.'+date[6:]
    subject = '[부동산 뉴스] ' + date
    copy_input_css('div.se-documentTitle p.se-text-paragraph', subject)
    time.sleep(2)
    driver.find_element_by_css_selector('div.se-section-text p.se-text-paragraph').click()
    time.sleep(1)
    for news in news_dic:
        element = WebDriverWait(driver, 5).until(  # 팝업 버
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.se-insert-point-marker-button"))
        )
        element.click()
        time.sleep(2)
        element = driver.find_element_by_css_selector("button.se-insert-menu-button-quotation")
        ActionChains(driver).move_to_element(element).click().perform() # not be scrolled into view 해결
        time.sleep(2)

        css1 = "ul.se-insert-menu-sub-panel-quotation button.se-insert-menu-sub-panel-button-quotation-quotation_line"
        eleme = driver.find_element_by_css_selector(css1)
        ActionChains(driver).move_to_element(eleme).click().perform()

        time.sleep(2)
        copy_input_css('span.se-placeholder.se-placeholder-focused', news)
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(driver).send_keys(Keys.RETURN).perform()
        time.sleep(1)

        pyperclip.copy(news_dic[news])
        time.sleep(2)
        ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
        # copy_input_css('div.se-section-text p.se-text-paragraph', news_dic[news])
        time.sleep(10)
    # driver.execute_script("window.scrollTo(0, document.body.scrollTop);")
    # subject = '[부의 길] ' + date + ' 부동산 뉴스'
    # subject_elem = driver.find_element_by_css_selector("div.se-container")
    # driver.execute_script("arguments[0].scrollIntoView(true);", subject_elem);
    # time.sleep(2)
    # copy_input_css('div.se-documentTitle p.se-text-paragraph', subject)


def publish():
    driver.find_element_by_css_selector('button.btn_publish').click()
    time.sleep(2)
    driver.find_element_by_css_selector('button.selectbox_button').click()
    time.sleep(2)
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.layer_list_option ul.list li:nth-child(4)"))
    )
    ActionChains(driver).move_to_element(element).click().perform()  # not be scrolled into view 해결
    time.sleep(2)
    driver.find_element_by_css_selector('button.btn_confirm').click()
    time.sleep(2)


if __name__ == "__main__":
    crawl_naver_main_news()
    get_real_press()
    make_dict()
    login()
    close_popup()
    write_blog()
    publish()
