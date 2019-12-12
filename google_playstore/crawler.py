# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 07:26:17 2018

@author: HongJea
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

#Download chrome driver from 'https://chromedriver.storage.googleapis.com/index.html?path=2.43/'
directory= r'C:\Users\ganda\Downloads\chromedriver_win32\chromedriver'
app_list= ['11st', 'auction', 'cgv', 'cjmall', 'coupang', 'G9', 'gmarket', 'gsshop', 'hmall', 'hnsmall', 'home plus', 'interpark', 'interpark ticket', 'lotte', 'lotte home shopping', 'lotte cinema', 'megabox', 'co kr quicket', 'tmon', 'we make price']

def execute_chrome(directory):
    driver= webdriver.Chrome(directory)
    driver.maximize_window()
    driver.implicitly_wait(3)
    return driver

def to_apppage(app_name):
    driver.get('https://play.google.com/store/apps')
    driver.find_element_by_css_selector('#gbqfq').send_keys(app_name)
    driver.find_element_by_css_selector('#gbqfb > span').click()
    time.sleep(waiting_time)
    driver.find_element_by_css_selector('#body-content > div > div > div.main-content > div > div:nth-child(1) > div > div.id-card-list.card-list.two-cards > div:nth-child(1) > div > div.cover > a > span.preview-overlay-container').click()
    driver.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div.XnFhVd > div > content > span').click()


def load_review(app_name):
    time_val= time.time()
    start_point= 0
    end_point= driver.execute_script("return document.body.scrollHeight")
    try:
        while time.time()< time_val+ 3600:
            while start_point!= end_point:
                start_point= end_point
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(waiting_time)
                end_point= driver.execute_script("return document.body.scrollHeight")
            driver.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz:nth-child(4) > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div:nth-child(2) > div.PFAhAf > div > content > span').click()
            time.sleep(waiting_time)
            end_point= driver.execute_script("return document.body.scrollHeight")
    except:
        print(app_name+ ' End')                             

def to_dataframe(app_name):
    html= driver.page_source
    soup= BeautifulSoup(html, 'html.parser')
                        
    body= soup.select('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div > div > div > div')
    
    user_name_list= []
    date_list= []
    comments_list= []
    rating_list= []
    app_name_list= []
    
    for i in range(0, len(body)):
        if len(body[i].findAll('div', {'class': {'UD7Dzf'}}))!=0:
            if len(body[i].findAll('div', {'class': {'pf5lIe'}}))!= 0:
                user_name_list.append(body[i].find('span', {'class': {'X43Kjb'}}).text)
                date_list.append(body[i].find('span', {'class': {'p2TkOb'}}).text)
                rating_list.append(str(body[i].find('div', {'role': {'img'}}).attrs)[26])
                comments_list.append(body[i].find('div', {'class': {'UD7Dzf'}}).text)
                app_name_list.append(app_name)
        
    data= {}
    data['user_name']= user_name_list
    data['date']= date_list
    data['comments']= comments_list
    data['rating']= rating_list
    data['app_name']= app_name_list
    data= pd.DataFrame(data, columns= ['user_name', 'date', 'comments', 'rating', 'app_name'])
    
    return data

waiting_time= 1.5
driver= execute_chrome(directory)

app_list= ['11st', 'auction', 'cgv', 'cjmall', 'coupang', 'G9', 'gmarket', 'gsshop', 'hmall', 'hnsmall', 'home plus', 'interpark', 'interpark ticket', 'lotte', 'lotte home shopping', 'lotte cinema', 'megabox', 'co kr quicket', 'tmon', 'we make price']

app= '11st'
for app in app_list:
    to_apppage(app_name= app)
    load_review(app_name= app)
    data= to_dataframe(app_name= app)
    data.to_csv(app+ '.csv', encoding= 'utf-8', index= False, sep= '\t')
    
driver.quit()
