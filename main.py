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
base_url = "https://land.naver.com"
url_for_date = "https://land.naver.com/news/headline.nhn" # 주요뉴스
date = ""
response = requests.get(url_for_date)
# if response.status_code == 200:
html = response.text
soup = BeautifulSoup(html, 'html.parser')
date_list = soup.select("span.num")
for elm in date_list:
    date += elm.text

url = url_for_date+"?bss_ymd="+date
# print(url) # 네이버 날짜별 주요뉴스 메인화면

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

link_list = []
news_title_list = []
main_news_list = soup.select("ul.headline_list > li > dl > dt:nth-of-type(2) > a") # 이미지가 없을경우 고려 안되어 있으

for link in main_news_list:
    link_list.append(base_url+link['href'])
    news_title_list.append(link.text)

# 뉴스 제목으로 실제 언론사 url 가져오기
news_query = 'https://search.naver.com/search.naver?where=news&query='
real_news_link = []
time.sleep(1)

for title in news_title_list:
    print(title)
    driver.get(news_query+title)
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a._sp_each_title"))
    )
    element.click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    new_url = driver.current_url
    real_news_link.append(new_url)
    print(new_url)
    driver.close();
    driver.switch_to.window(driver.window_handles[0])



driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https://blog.naver.com/shn413')

def copy_input_xpath(xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    time.sleep(2)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
    
def copy_input_css(css, input):
    pyperclip.copy(input)
    driver.find_element_by_css_selector(css).click()
    time.sleep(2)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
    time.sleep(2)
    pyperclip.copy("\n")
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
# 로그인    
id = "shn413"
pw = "ekqlscl12!@"

copy_input_xpath('//*[@id="id"]', id)
copy_input_xpath('//*[@id="pw"]', pw)

driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
time.sleep(2)
driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="mainFrame"]'))

# 글쓰기 버튼 클릭
element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div#post-admin a.col._checkBlock._rosRestrict"))
)
element.click()
time.sleep(2)
# driver.switch_to.frame(driver.find_element_by_id('blog-editor'))

### 작성중인 글 팝업 예외처리 필요
subject = '[부의 길] '+date+' 부동산 뉴스'
copy_input_css('div.se-documentTitle p.se-text-paragraph', subject)
time.sleep(1)
css = 'div.se-section-text p.se-text-paragraph'

# for link in link_list:
for link in real_news_link:
    copy_input_css('div.se-section-text p.se-text-paragraph', link)
