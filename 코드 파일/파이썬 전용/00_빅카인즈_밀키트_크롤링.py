#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install selenium


# In[3]:


pip install xmltodict


# In[6]:


import pandas as pd
import json
import pandas as pd
import re
from urllib.request import urlopen
import xmltodict

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from time import sleep
import math

import os

# 단어 사아의 공백으로 번위 20190101 ~ 20200930
keyword = "밀키트"
# start_day = "2017-12-26"
start_day = "2021-08-01"
#start_day = "2020-02-01"
end_day = "2021-08-08"# 미만


class Search_BigKinds:
    '''
    
    빅카인즈 크롤링 하는 클래스
    
    '''
    click_time = 1.5
    send_time = 0.5
    date_time = 2 # 날짜 변경해서 새로 driver를 켤 때 변경시간
    wait_time = 10 # 오류 발생시 기다리는 시간
    def __init__(self):
        '''
            기본 드라이브 실행
        '''
        # create a new chrome session
        prefs = {'profile.default_content_setting_values': {'cookies' : 2,
                         'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2,
                         'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2,
                         'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2,
                         'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2,
                         'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2,
                         'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}
        options = Options()
        # options.add_experimental_option('prefs', prefs) 
        # options.add_argument("start-maximized") 
        # options.add_argument("disable-infobars") 
        # options.add_argument("--disable-extensions")
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        
        self.Crawling_news = dict({"Date":[],"Title":[],"Content":[]})
        
        try:
            self.driver = webdriver.Chrome(options=options, executable_path="C:\\Users\\nj425\\AppData\\Local\\SeleniumBasic\\chromedriver.exe");sleep(self.date_time)
        except:
            sleep(self.wait_time)  
            self.driver = webdriver.Chrome(options=options, executable_path="C:\\Users\\nj425\\AppData\\Local\\SeleniumBasic\\chromedriver.exe");sleep(self.date_time)
        self.driver.implicitly_wait(self.wait_time)
        self.driver.maximize_window()

        url = "https://www.bigkinds.or.kr/"
        try:
            self.driver.get(url);sleep(self.date_time)
        except:
            sleep(self.wait_time)
            self.driver.get(url);sleep(self.date_time)
            

    def Search_keyword(self,keyword,start_day,end_day):
        self.keyword = keyword
        self.start_day = start_day
        self.end_day = end_day
        
        # 키워드 입력
        try:
            self.driver.find_element(By.CLASS_NAME, 'search-key').send_keys(keyword);sleep(self.send_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.CLASS_NAME, 'search-key').send_keys(keyword);sleep(self.send_time)

        # 상세 검색
        try:
            self.driver.find_element(By.CLASS_NAME, 'btn-srchDetail.btn-srchDetail-search').click();sleep(self.click_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.CLASS_NAME, 'btn-srchDetail.btn-srchDetail-search').click();sleep(self.click_time)
        
        # 기간 메뉴
        try:
            self.driver.find_element(By.CLASS_NAME, 'tab-btn.search-tab_group').click();sleep(self.click_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.CLASS_NAME, 'tab-btn.search-tab_group').click();sleep(self.click_time)
        
        # 시작 기간
        try:
            self.driver.find_element(By.ID, 'search-begin-date').send_keys("\b\b\b\b\b\b\b\b\b\b{}".format(start_day));sleep(self.send_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.ID, 'search-begin-date').send_keys("\b\b\b\b\b\b\b\b\b\b{}".format(start_day));sleep(self.send_time)
            
        # 끝 기간
        try:
            self.driver.find_element(By.ID, 'search-end-date').send_keys("\b\b\b\b\b\b\b\b\b\b{}".format(end_day));sleep(self.send_time)
        except:
            sleep(self.wait_time)
            self.driver.find_element(By.ID, 'search-end-date').send_keys("\b\b\b\b\b\b\b\b\b\b{}".format(end_day));sleep(self.send_time)
        
        self.driver.find_element(By.CLASS_NAME, 'btn-srch.input-group-btn.news-search-btn').click();sleep(self.click_time)
            
        try:
            self.total_cnt = int(re.sub(',','',self.driver.find_element(By.CLASS_NAME, 'total-news-cnt').text))
        except:
            sleep(self.wait_time)
            self.total_cnt = int(re.sub(',','',self.driver.find_element(By.CLASS_NAME, 'total-news-cnt').text))
        self.total_page = math.ceil(self.total_cnt/10)
        print("총 데이터 개수 : ",self.total_cnt)
        print("총 페이지 개수 : " ,self.total_page)

    def pages(self):
        '''
            모든 페이지를 크롤링
        '''
        lastPage = self.driver.find_element(By.CLASS_NAME, 'lastNum').text
        # 현재 페이지
        isLastPage = False
        curPage=1
        while(not isLastPage):


            ## 페이지 크롤링
            self.page_crawling_news()

            if curPage == int(lastPage):
                isLastPage = True
            else:
                self.driver.find_element(By.CLASS_NAME, 'page-next.page-link').click()
                sleep(self.click_time)
                curPage+=1
        
    def page_crawling_news(self):
        '''
            현재 페이지의 뉴스 내용을 크롤링
        '''


        articles = self.driver.find_element(By.ID, 'news-results')
        for i in range(1,len(articles.find_elements_by_class_name('news-item'))+1):

            #뉴스 클릭
            try:
                self.driver.find_element(By.XPATH, f'//*[@id="news-results"]/div[{i}]/div/div[2]/a/div/strong/span').click();sleep(self.click_time)
            except:
                sleep(self.wait_time)
                self.driver.find_element(By.XPATH, f'//*[@id="news-results"]/div[{i}]/div/div[2]/a/div/strong/span').click();sleep(self.click_time)     
                   
            #날짜 가져오기
            try:
                date = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/div[1]/ul/li[1]').text;sleep(self.click_time)
            except:
                sleep(self.click_time)
                date = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/div[1]/ul/li[1]').text;sleep(self.click_time)

            #제목 가져오기           
            try:
                title = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/h1').text;sleep(self.click_time)
            except:
                sleep(self.click_time)
                title = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[1]/h1').text;sleep(self.click_time)

            #기사 내용 가져오기                
            try:
                content = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[2]').text;sleep(self.click_time)
            except:
                sleep(self.click_time)
                content = self.driver.find_element(By.XPATH, f'//*[@id="news-detail-modal"]/div/div/div[1]/div/div[2]').text;sleep(self.click_time)
            
            
            
            self.Crawling_news["Date"].append(date)
            self.Crawling_news["Title"].append(title)
            self.Crawling_news["Content"].append(content)

            #닫힘 버튼 누르기
            try:
                self.driver.find_element(By.XPATH, '//*[@id="news-detail-modal"]/div/div/button').click();sleep(self.click_time)
            except:
                sleep(self.wait_time)
                self.driver.find_element(By.XPATH, '//*[@id="news-detail-modal"]/div/div/button').click();sleep(self.click_time)            

            
    def display(self):
        '''
        기본 정보
        '''
        print("키워드 : ",self.keyword,", 기간 : {} ~ {}".format(self.start_day,self.end_day))
        print("총 페이지 수 : ",self.total_page,"총 데이터 수 : ",self.total_cnt)
    
    def Save(self):
        '''
        
        데이터 저장
        
        '''
        s_d  = self.start_day[:4]+self.start_day[5:7]+self.start_day[-2:]
        e_d  = self.end_day[:4]+self.end_day[5:7]+self.end_day[-2:]
        pd.DataFrame(self.Crawling_news).to_csv("./빅카인즈/{}_{}_{}.csv".format(self.keyword,s_d,e_d),index=False)

        
# 단어 사아의 공백으로 번위 20190101 ~ 20200930
keyword = "밀키트"
start_day = "2021-08-01"
end_day = "2021-08-08"# 미만

if not os.path.exists("./빅카인즈"):
    os.makedirs("./빅카인즈")

try:
    Search = Search_BigKinds()
    Search.Search_keyword(keyword,start_day,end_day)
    try:
        Search.pages()
    except:
        try:
            print("오류... 다시 시도 중...")
            sleep(Search.wait_time)
            Search.wait_time = 30
            Search.pages()
        except:
            print("오류... 다시 시도 중...")
            sleep(Search.wait_time)
            Search.wait_time = 60
            Search.pages()
    Search.Save()
    Search.display()
    Search.driver.close()
    sleep(Search.date_time)
except:
    print("오류 발생 종료 {}".format(day))
    del Search


# In[ ]:


#크롤링 결과 확인
df = pd.read_csv('./빅카인즈/밀키트_20210801_20210808.csv')
df

