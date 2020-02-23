import requests
from bs4 import BeautifulSoup

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
#     print(url) # 날짜별 주요뉴스

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

total_list = []
main_news_list = soup.select("ul.headline_list > li > dl > dt:nth-of-type(1) > a")
for link in main_news_list:
    total_list.append(base_url+link['href'])
#     print(base_url+link['href'])

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import time

def copy_input(xpath, input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    time.sleep(2)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
    
def copy_input2(css, input):
    pyperclip.copy(input)
    driver.find_element_by_css_selector(css).click()
    time.sleep(2)
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
    
driver = webdriver.Firefox(capabilities=None, executable_path='/usr/local/bin/geckodriver')
driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https://blog.naver.com/shn413')

id = "shn413"
pw = "ekqlscl12!@"

copy_input('//*[@id="id"]', id)
copy_input('//*[@id="pw"]', pw)

driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
time.sleep(2)
driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="mainFrame"]'))

# 글쓰기 버튼
# driver.find_element_by_css_selector('div#post-admin a.col._checkBlock._rosRestrict').click()
element = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div#post-admin a.col._checkBlock._rosRestrict"))
)
element.click()
# driver.switch_to.default_content()
time.sleep(2)
subject = '[부의 길] - 2020.02.21(금) 부동산 뉴스'
# copy_input2('div.se-documentTitle p.se-text-paragraph', subject)
time.sleep(1)
for link in total_list:
    copy_input2('div.se-section-text p.se-text-paragraph', link)
    time.sleep(3)
# copy_input2('div.se-section-text p.se-text-paragraph', "https://land.naver.com/news/newsRead.nhn?type=headline&bss_ymd=20200222&prsco_id=119&arti_id=0002384343")




