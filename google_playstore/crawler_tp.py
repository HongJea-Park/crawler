# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 07:26:17 2018

@author: HongJea
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd


class google_play:
    #Download chrome driver from 'https://chromedriver.storage.googleapis.com/index.html?path=2.43/'
    directory= r'C:\Users\HongJea\Desktop\Workspace\chromedriver'
    waiting_time= 1.5
    
    def execute_chrome(self):
        driver= webdriver.Chrome(self.directory)
        driver.maximize_window()
        driver.implicitly_wait(1.5)
        return driver
    
    
    def to_apppage(self, app_name):
        driver.get('https://play.google.com/store/apps')
        driver.find_element_by_css_selector('#gbqfq').send_keys(app_name)
        driver.find_element_by_css_selector('#gbqfb > span').click()
        driver.find_element_by_css_selector('#body-content > div > div > div.main-content > div > div:nth-child(1) > div > div.id-card-list.card-list.two-cards > div:nth-child(1) > div > div.cover > a > span.preview-overlay-container').click()
        driver.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div.XnFhVd > div > content > span').click()
        driver.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div > c-wiz > div > div > div > div.CeEBt.Ce1Y1c.eU809d > span').click()
        driver.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div > c-wiz > div > div > div.OA0qNb.ncFHed > div').click()
    
    
    def load_page(self, app_name, time_limit):
        start_point= 0
        end_point= driver.execute_script("return document.body.scrollHeight")
        start_time= time.time()
        try:
            while time.time()- start_time< time_limit:
                while start_point!= end_point:
                    start_point= end_point
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(self.waiting_time)
                    end_point= driver.execute_script("return document.body.scrollHeight")
                driver.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz:nth-child(4) > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div:nth-child(2) > div.PFAhAf > div > content > span').click()
                time.sleep(self.waiting_time)
                end_point= driver.execute_script("return document.body.scrollHeight")
        except:
            print(app_name+ ' End')                             
        
    
    def date_finder(self):
        html= driver.page_source
        soup= BeautifulSoup(html, 'html.parser')
        body= soup.select('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div > div > div > div')
        date= body[-1].find('span', {'class': {'p2TkOb'}}).text
        return date
    
    
    def datetime(self, date):
        date= pd.to_datetime(date.strip().replace('년', '-').replace('월', '-').replace('일', '').replace(' ', ''), format= '%Y%m%d', errors= 'ignore')
        return date
    
    
    def to_dataframe(self, app_name, save_option= True):
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
        df= {}
        df['user_name']= user_name_list
        df['date']= date_list
        df['comments']= comments_list
        df['rating']= rating_list
        df['app_name']= app_name_list
        df= pd.DataFrame(df, columns= ['user_name', 'date', 'comments', 'rating', 'app_name'])
        df['date']= df['date'].apply(lambda x: self.datetime(x))
        if save_option== True:
            df.to_csv(r'reviews\\origin\\'+ app_name+ '.csv', encoding= 'utf-8', sep= '\t', index= False)
        return df
    
    
    def close_driver(self):
        driver.quit()
        
        
    def date_filter(self, app_name, df, start_date, save_option= True):
        df= df[df['date']> pd.to_datetime(start_date, format= '%Y%m%d', errors= 'ignore')]
        if save_option== True:
            df.to_csv(r'reviews\\date_filtered\\'+ app_name+ '.csv', encoding= 'utf-8', sep= '\t', index= False)
        return df


    def concat(self, app_list, review_type= 'date_filtered', save_option= False):
        total_review= pd.DataFrame()
        for app in app_list:
            reviews= pd.read_csv('reviews\\'+ review_type+ '\\'+ app+ '.csv', sep= '\t', encoding= 'utf-8', engine= 'python')
            total_review= pd.concat([total_review, reviews], axis= 0, ignore_index= True)    
        if save_option== True:
            total_review.to_csv('reviews\\'+ review_type+ '\\'+ 'total_review.csv', sep= '\t', encoding= 'utf-8', index= False)
        return total_review


app_list= pd.read_csv('App_Annie\\App_Annie_상위앱차트순위(2018-12-01~2019-01-31).csv', sep= ',', encoding= 'cp949', engine= 'python')['app_name'][0:30]
app_list= app_list.str.replace('/', ',')
crawler= google_play()
for app in app_list[0:]:
    driver= crawler.execute_chrome()
    crawler.to_apppage(app_name= app)
    crawler.load_page(app_name= app, time_limit= 7200)
    df= crawler.to_dataframe(app_name= app, save_option= True)
    df= crawler.date_filter(app_name= app, df= df, start_date= '2017-01-01', save_option= True)    
    crawler.close_driver()

df= crawler.concat(app_list, review_type= 'origin', save_option= True)
df= crawler.concat(app_list, review_type= 'date_filtered', save_option= True)
