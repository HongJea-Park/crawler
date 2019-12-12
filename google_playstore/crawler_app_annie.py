# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 15:59:38 2019

@author: HongJea
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import pandas as pd

directory= r'C:\Users\HongJea\Desktop\Workspace\chromedriver'
waiting_time= 1.5
    
driver= webdriver.Chrome(directory)
driver.maximize_window()
driver.implicitly_wait(1.5)

driver.get('https://www.appannie.com/dashboard/home/')
driver.find_element_by_css_selector('#email').send_keys('ganda9220@naver.com')
driver.find_element_by_css_selector('#password').send_keys('ghdwp5@41')
driver.find_element_by_css_selector('#submit').click()

min_date= datetime.now().date()- timedelta(days= 90)
start_date= datetime(2018, 12, 1).date()
end_date= datetime(2019, 1, 31).date()
end_date= datetime.now().date()
date_range= pd.date_range(start_date, end_date)

for date in date_range:
    driver.get('https://www.appannie.com/apps/google-play/top-chart/?country=KR&category=30&device=&date='+ str(date.date())+ '&feed=All&rank_sorting_type=rank&page_number=0&page_size=100&table_selections=')
    time.sleep(3)
    html= driver.page_source
    soup= BeautifulSoup(html, 'html.parser')
    body= soup.select('#sub-container > div.main.storestats_wrapper.page_top > div.inner > div.frame.frame-ss > div > div > div > div > div > app-group-table-container > div > div.ng-isolate-scope > div > div.dashboard-table.ng-scope > div > table > tbody > tr')
    rank_list= []
    app_list= []    
    for i in range(0, 100):
        rank_list.append(i+ 1)
        app_list.append(body[i].find('div', {'class': {'app-link-container'}}).text[2:-2].strip().replace('\u2013', '').replace('\u5b9d', ''))    
    df= {}
    df['rank']= rank_list
    df['app_name']= app_list
    df= pd.DataFrame(df, columns= ['rank', 'app_name'])
    df.to_csv('App_Annie\\'+ str(date.date())+ '기준_App_Annie_상위앱차트.csv', sep= ',', encoding= 'cp949', index= False)
driver.quit()


df= pd.DataFrame()
for date in date_range:
    temp= pd.read_csv('App_Annie\\'+ str(date.date())+ '기준_App_Annie_상위앱차트.csv', sep= ',', encoding= 'cp949', engine= 'python')
    df= pd.concat([df, temp], axis= 0)    

df['points']= 101- df['rank']
df= df[['app_name', 'rank', 'points']]
dff= df.groupby(df['app_name']).sum().sort_index()
dff['date_count']= df['app_name'].value_counts()
dff= dff.reset_index(drop= False)
dff= dff.sort_values(by= 'points', ascending= False).reset_index(drop= True)
dff= dff['app_name'].str.replace('/', ',')
dff.to_csv('App_Annie\\App_Annie_상위앱차트순위(2018-12-01~2019-01-31).csv', sep= ',', encoding= 'cp949', index= False)

dff.sort_values(by= 'rank')


