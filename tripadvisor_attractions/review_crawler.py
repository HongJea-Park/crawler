# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 00:35:42 2019

@author: hongj
"""

import time
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('review_crawler.py'))))
from crawler import spot_info_crawler
from tqdm import tqdm

waiting_time_for_loading= 2
waiting_time_for_user_info= 0.5

def get_review_inpage(driver):
    
    '''
    A function for crawling review, date, user information, etc.
    
    ---Parameter---
    driver: Web Driver
    '''
    
    user_history5= []
    user_history4= []
    user_history3= []
    user_history2= []
    user_history1= []
    title= []
    date= []
    comment= []
    rating= []
    
    reviewid_list= [reviewSelector.get_attribute('data-reviewid') \
                    for reviewSelector in driver.find_elements_by_class_name('reviewSelector')]
    
    while None in reviewid_list:
        reviewid_list.remove(None)
        
    show_more= False
    
    for reviewid in reviewid_list:
        more= '#review_%s > div > div.ui_column.is-9 > div.prw_rup.prw_reviews_text_summary_hsx > div > p > span'%reviewid
        
        if not show_more:
            
            try:
                driver.find_element_by_css_selector(more).click()
                show_more= True
                time.sleep(waiting_time_for_user_info)
                
            except:
                pass
            
        userinfo_selector= '#review_%s> div > div.ui_column.is-2.memberInfoColumn > div > div'%reviewid
        userid= driver.find_elements_by_css_selector(userinfo_selector)[0].find_elements_by_css_selector('*')[0].get_attribute('id')
        
        if userid== '':
            continue
        
        userinfo_selector= '#%s'%userid
        driver.find_element_by_css_selector(userinfo_selector).click()
        
        try:
            user_history5.append(int(driver.find_element_by_css_selector('#BODY_BLOCK_JQUERY_REFLOW > span > div.body_text > div > div > div > div.wrap > div > ul > div:nth-child(1) > span.rowCountReviewEnhancements.rowCellReviewEnhancements').text))
            user_history4.append(int(driver.find_element_by_css_selector('#BODY_BLOCK_JQUERY_REFLOW > span > div.body_text > div > div > div > div.wrap > div > ul > div:nth-child(2) > span.rowCountReviewEnhancements.rowCellReviewEnhancements').text.replace(' ', '')))
            user_history3.append(int(driver.find_element_by_css_selector('#BODY_BLOCK_JQUERY_REFLOW > span > div.body_text > div > div > div > div.wrap > div > ul > div:nth-child(3) > span.rowCountReviewEnhancements.rowCellReviewEnhancements').text.replace(' ', '')))
            user_history2.append(int(driver.find_element_by_css_selector('#BODY_BLOCK_JQUERY_REFLOW > span > div.body_text > div > div > div > div.wrap > div > ul > div:nth-child(4) > span.rowCountReviewEnhancements.rowCellReviewEnhancements').text.replace(' ', '')))
            user_history1.append(int(driver.find_element_by_css_selector('#BODY_BLOCK_JQUERY_REFLOW > span > div.body_text > div > div > div > div.wrap > div > ul > div:nth-child(5) > span.rowCountReviewEnhancements.rowCellReviewEnhancements').text.replace(' ', '')))
                                                                         
        except:
            user_history5.append(0)
            user_history4.append(0)
            user_history3.append(0)
            user_history2.append(0)
            user_history1.append(0)
            
        driver.find_element_by_css_selector('#BODY_BLOCK_JQUERY_REFLOW > span > div.ui_close_x').click()     
                                            
        base_selector= '#review_%s > div > div.ui_column.is-9 > '%reviewid
        date_selector= 'span.ratingDate'
        title_selector= '#rn%s > span'%reviewid
        comment_selector= 'div.prw_rup.prw_reviews_text_summary_hsx > div > p'
        rating_selector= 'span.ui_bubble_rating'
        
        title.append(driver.find_element_by_css_selector(title_selector).text)
        date.append(driver.find_element_by_css_selector(base_selector+ date_selector).get_attribute('title'))
        comment.append(driver.find_element_by_css_selector(base_selector+ comment_selector).text)
        rating.append(int(driver.find_element_by_css_selector(base_selector+ rating_selector).get_attribute('class')[-2:])/ 10)
        
    return user_history1, user_history2, user_history3, user_history4, user_history5, title, date, comment, rating



def next_page(driver, page, final_page):
    
    '''
    A function for going to the next page
    
    ---parameter---
    driver: Web driver
    page: Current page
    final_page: Final page for a specific spot
    '''
    
    if page== 1:
        driver.find_element_by_css_selector('#taplc_location_reviews_list_resp_ar_responsive_0 > div > div:nth-child(15) > div > div > a.nav.next.taLnk.ui_button.primary').click()
                                            
    elif page!= final_page:
        driver.find_element_by_css_selector('#taplc_location_reviews_list_resp_ar_responsive_0 > div > div:nth-child(14) > div > div > a.nav.next.taLnk.ui_button.primary').click()
                                            
    time.sleep(waiting_time_for_loading)

def get_review(driver, url, spot):
    
    '''
    A function to get review for spot.
    
    This function is repeated until all work has been completed and does not stop if an network error occurs.
    
    If you fall in a loop from one page, you should scroll down the driver and the work will be continued.
    
    ---parameter---
    driver: Web driver
    url: URL for specific spot
    spot: Spot name
    '''
    
    user_history5_list= []
    user_history4_list= []
    user_history3_list= []
    user_history2_list= []
    user_history1_list= []
    title_list= []
    date_list= []
    comment_list= []
    rating_list= []
    
    driver.get(url)
    time.sleep(waiting_time_for_loading)
    
    try:
        final_page= int(driver.find_element_by_css_selector('#taplc_location_reviews_list_resp_ar_responsive_0 > div > div:nth-child(15) > div > div > div').find_elements_by_css_selector('*')[-1].get_attribute('data-page-number'))
                                                            
    except:
        final_page= 1
        
    for page in tqdm(range(1, final_page+ 1)):
        page_url= driver.current_url
        
        while True:
            try:
                user_history1, user_history2, user_history3, user_history4, user_history5, title, date, comment, rating\
                = get_review_inpage(driver)                
                
                user_history5_list.extend(user_history5)
                user_history4_list.extend(user_history4)
                user_history3_list.extend(user_history3)
                user_history2_list.extend(user_history2)
                user_history1_list.extend(user_history1)
                title_list.extend(title)
                date_list.extend(date)
                comment_list.extend(comment)
                rating_list.extend(rating)
                
                if page!= final_page:
                    next_page(driver, page, final_page)
                    
                else:
                    pass
                
                if len(user_history5_list)!= len(title_list):
                    raise NotImplementedError
                    
            except:
                driver.get(page_url)
                time.sleep(waiting_time_for_loading)
                
                _, y_loc= driver.find_element_by_css_selector('#taplc_location_reviews_list_resp_ar_responsive_0 > div > div.pagination-details').location.values()
                                                              
                driver.execute_script('window.scrollTo(0, %s);'%(y_loc- 500))
                time.sleep(waiting_time_for_loading)
                
                continue
            
            break
        
    spot_list= [spot for l in range(len(comment_list))]
    
    df= {}
    df['title']= title_list
    df['date']= date_list
    df['comment']= comment_list
    df['user_history1']= user_history1_list
    df['user_history2']= user_history2_list
    df['user_history3']= user_history3_list
    df['user_history4']= user_history4_list
    df['user_history5']= user_history5_list
    df['rating']= rating_list
    df['spot']= spot_list
    
    df= pd.DataFrame(df, columns= ['title', 'date', 'comment', 'user_history1', 'user_history2', 'user_history3', \
                                   'user_history4', 'user_history5', 'rating', 'spot'])
    
    df.to_csv('../reviews/%s.csv'%spot, sep= ',', encoding= 'utf-8', index= False)


if __name__== "__main__":
    
    spot_info= pd.read_csv('../results/spot_info.csv', encoding= 'utf-8', sep= ',')
    driver= spot_info_crawler.open_chrome()
    driver.implicitly_wait(2)

    spot_info.spot= spot_info.spot.map(lambda x: x.replace(' ', '_'))
    spot_info.spot.iloc[92]= 'COEX_Center_0'
    spot_info.spot.iloc[177]= 'COEX_Center_1'
    spot_info.to_csv('../results/spot_info.csv', sep= ',', encoding= 'utf-8', index= False)
    
    for i in range(10, -1, -1):
        url= spot_info.url[i]
        spot= spot_info.spot[i]
        get_review(driver, url, spot)
    