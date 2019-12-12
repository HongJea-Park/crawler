# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 16:17:35 2019

@author: hongj
"""

from selenium import webdriver
import time
import pandas as pd

directory= r'D:\D_Workspace\chromedriver.exe'
waiting_time= 1.5

def open_chrome():
    
    '''
    A function for executing chrome and maximize window.
    Because there are web pages that location of some elements are changed by window size.
    '''
    
    driver= webdriver.Chrome(directory)
    driver.maximize_window()
    driver.implicitly_wait(3)
    
    return driver

def get_spot_list(url, end_page):
    
    '''
    A function to get spot information at tripadvisor by location
    
    ---Parameter---
    url: Things to do page in tripadvisor 
    
    '''
    
    driver.get(url)
    
    if end_page> 29: 
        end_page= 29
    
    element_selector= '#FILTERED_LIST > div.attractions-attraction-overview-pois-PoiGrid__wrapper--2H3Mo > li > div.attractions-attraction-overview-pois-PoiCard__card_info--3scTT > div'
    url_selector= '#FILTERED_LIST > div.attractions-attraction-overview-pois-PoiGrid__wrapper--2H3Mo > li > div.attractions-attraction-overview-pois-PoiCard__card_info--3scTT > div > div:nth-child(1) > div:nth-child(3) > a'
    see_more_selector= '#FILTERED_LIST > div.attractions-attraction-overview-main-TopPOIs__see_more--2Vsb-'
    
    category_TA= [driver.find_elements_by_css_selector(element_selector)[i].text.split('\n')[0] for i in range(10)]
    spot= [driver.find_elements_by_css_selector(element_selector)[i].text.split('\n')[1] for i in range(10)]
    num_review= [int(driver.find_elements_by_css_selector(element_selector)[i].text.split('\n')[2].replace('reviews', '').replace(' ', '')) for i in range(10)]
    url= [driver.find_elements_by_css_selector(url_selector)[i].get_attribute('href') for i in range(10)]
    driver.find_element_by_css_selector(see_more_selector).click()
    
    time.sleep(3)
    
    for i in range(20):
        element_selector= '#FILTERED_LIST > div:nth-child(3) > div > li > div.attractions-attraction-overview-pois-PoiCard__card_info--3scTT > div > div:nth-child(1)'
        url_selector= '#FILTERED_LIST > div:nth-child(3) > div > li > div.attractions-attraction-overview-pois-PoiCard__card_info--3scTT > div > div:nth-child(1) > div:nth-child(3) > a'
        next_page_selector= '#FILTERED_LIST > div:nth-child(5) > div > div.attractions-attraction-overview-main-Pagination__container--PUXGq > div:nth-child(4) > a'
        
        category_TA.append(driver.find_elements_by_css_selector(element_selector)[i].text.split('\n')[0])
        spot.append(driver.find_elements_by_css_selector(element_selector)[i].text.split('\n')[1])
        num_review.append(int(driver.find_elements_by_css_selector(element_selector)[i].text.split('\n')[2].replace('reviews', '').replace(' ', '')))
        url.append(driver.find_elements_by_css_selector(url_selector)[i].get_attribute('href'))
        
    driver.find_element_by_css_selector(next_page_selector).click()
    
    time.sleep(3)
    
    if end_page>= 2:
        next_page= 1
        
        for p in range(2, end_page+ 1):
            
            if p>= 5: next_page= 4
            
            for i in range(30):
                page_list_selector= '#FILTERED_LIST > div.al_border.deckTools.btm > div > div > div'
                category_TA.append(driver.find_elements_by_class_name('flexible')[i].text.split('\n')[0])
                spot.append(driver.find_elements_by_class_name('flexible')[i].text.split('\n')[1])
                num_review.append(int(driver.find_elements_by_class_name('flexible')[i].text.split('\n')[2].replace('reviews', '').replace(' ', '')))
                url.append(driver.find_elements_by_class_name('flexible')[i].find_elements_by_tag_name('a')[-1].get_attribute('href'))
                
            page_list= driver.find_element_by_css_selector(page_list_selector).find_elements_by_tag_name('a')
            page_list[next_page].click()
            time.sleep(3)
            next_page+= 1
            
    return category_TA, spot, num_review, url

if __name__== "__main__":
    init_url= 'https://www.tripadvisor.co.za/Attractions-g294197-Activities-Seoul.html'
    driver= open_chrome()
    category_TA, spot, num_review, url= get_spot_list(init_url, 10)
    
    df= pd.DataFrame()
    df['spot']= spot
    df['category_TA']= category_TA
    df['num_review']= num_review
    df['url']= url
    
    df.to_csv(r'../results/spot_info.csv', sep= ',', encoding= 'utf-8', index= False)
