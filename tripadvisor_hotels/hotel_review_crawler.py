# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 14:23:38 2019

@author: hongj
"""

from selenium import webdriver
import time
import pandas as pd
from tqdm import tqdm
import re


class hotel_url_crawler():
    
    
    def __init__(self, driver_directory, list_url):
        
        options= webdriver.ChromeOptions()
#        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        
        self.waiting_time_= 1
        self.list_url_= list_url
        self.driver= webdriver.Chrome(driver_directory, chrome_options= options)
        self.driver.implicitly_wait(3)
        self.driver.get(self.list_url_)
        self.url_list_= []
        
        self.endpage_selector_= '#taplc_main_pagination_bar_dusty_hotels_resp_0 > div > div > div > div > a.pageNum.last.taLnk'
        self.next_page_selector_= '#taplc_main_pagination_bar_dusty_hotels_resp_0 > div > div > div > a.nav.next.taLnk.ui_button.primary'
        self.empty_selector_= '#HEADING > h1'
        self.hotel_list_selector_= '#taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0 > div > div > div.meta_listing.ui_columns.large_thumbnail_mobile > div.ui_column.is-8.main_col.allowEllipsis > div.main-cols > div.info-col > div.prw_rup.prw_common_rating_and_review_count_with_popup.linespace.is-shown-at-mobile > a.review_count'
        self.question_box_selector_= '#BODY_BLOCK_JQUERY_REFLOW > div.QSISlider.SI_6yB28yrnSys18xf_SliderContainer > div:nth-child(8) > div'
        
        time.sleep(self.waiting_time_* 5)

        
    def get_endpage_info(self):

        return int(self.driver.find_element_by_css_selector(self.endpage_selector_).text)
        
        
    def click_empty(self):
        
        self.driver.find_element_by_css_selector(self.empty_selector_).click()
        
    
    def next_page(self):
        
        self.driver.find_element_by_css_selector(self.next_page_selector_).click()
        
        
    def get_reviewlist_url(self):
        
        hotel_list_= self.driver.find_elements_by_css_selector(self.hotel_list_selector_)
        
        for hotel_ in hotel_list_:
            
            self.url_list_.append(hotel_.get_attribute('href'))
                
    
    def detect_question_box(self):
        
        question_box_= self.driver.find_elements_by_css_selector(self.question_box_selector_)
        
        if len(question_box_)!= 0:
            question_box_[0].click()
    
    
    def execute(self):
        
        self.get_reviewlist_url()
        self.endpage_= self.get_endpage_info()
        
        retry_= 0
        
        for i in tqdm(range(self.endpage_- 1)):
            
            current_page_= self.driver.current_url

            
            while True:
            
                try: 
                    self.next_page()
                    
                except:

                    retry_+= 1
                    
                    if retry_%10== 0:
                        self.driver.get(current_page_)
                    
#                    if retry_%20== 0:
#                        self.detect_question_box()
                    
                    print('error type 1')
                        
                    time.sleep(self.waiting_time_)
                    
                    continue
                
                retry_= 0
                
                break
            
            while True:
                
                try:
                    self.get_reviewlist_url()
                    
                except:

                    print('error type 2')
                    
                    retry_+= 1
                    if retry_%10== 0: self.driver.get(current_page_)
                    
                    time.sleep(self.waiting_time_)

                    continue
                
                retry_= 0
                
                break
            
        self.url_list_= [url for url in list(set(self.url_list_)) if not url is None]
        self.driver.close()
    
        
class review_crawler():
    
    
    def __init__(self, driver_directory, hotel_url, current_month, current_year):

        options= webdriver.ChromeOptions()
#        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        
        self.waiting_time_= 1.5
        self.hotel_url_= hotel_url
        self.driver= webdriver.Chrome(driver_directory, chrome_options= options)
        self.driver.implicitly_wait(3)
        self.driver.get(self.hotel_url_)

        self.hotel_name_selector_= '#HEADING'
        
        self.read_more_class_name_= 'hotels-review-list-parts-ExpandableReview__cta--3U9OU'
        self.location_class_name_= 'hotels-review-list-parts-ReviewSearchTextInput__wrapper--Wlmd3'
        self.select_eng_class_name_= 'hotels-review-list-parts-LanguageFilter__no_wrap--3zMxR'
        self.num_reviews_class_name_= 'hotels-review-list-parts-LanguageFilter__paren_count--EHwQo'
        self.page_list_class_name_= 'ui_pagination'
        self.ui_class_name_= 'ui_button'
        self.reviewlist_class_name_= 'hotels-community-tab-common-Card__card--ihfZB'
        self.reviewlist_class_name_= 'hotels-community-tab-common-Card__card--ihfZB'
        self.writer_class_name_= 'social-member-event-MemberEventOnObjectBlock__event_type--3njyv'
        self.rating_class_name_= 'ui_bubble_rating'
        self.review_class_name_= 'hotels-review-list-parts-ExpandableReview__reviewText--3oMkH'
        self.stay_class_name_= 'hotels-review-list-parts-EventDate__event_date--CRXs4'
        self.endpage_class_name_= 'pageNum'
        self.star_class_name_= 'ui_star_rating'
        self.price_class_name_= 'hotels-hotel-review-persistent-header-and-footer-TabsDesktop__commerce--3-tZq'
        
        self.hotel_name_list_= []
        self.hotel_star_list_= []
        self.hotel_price_list_= []
        self.review_list_= []
        self.rating_list_= []
        self.date_list_= []
        self.writer_list_= []
        self.stay_list_= []
        
        self.rating_table_= {'_1Nb7S6iu': 1,
                             '_1LNKWH49': 2,
                             '_17GUOtor': 3,
                             '_7BtjwjjB': 4,
                             'dnQ8TT87': 5}
        
        self.month_list_= ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', \
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.current_month_= current_month
        self.current_year_= current_year
        
        self.save= False
        self.retry_= 0
        
            
    def get_endpage_info(self):
        
        return int(self.driver.find_elements_by_class_name(self.endpage_class_name_)[-1].text)
        
        
    def select_eng(self):
        
        while True:
            
            try:
                
                self.page_move()

                langlist= self.driver.find_elements_by_class_name(self.select_eng_class_name_)
                
                eng= None
                
                for i, l in enumerate(langlist):
                    
                    if l.text== 'English': 
                        eng= l
                        self.language_idx_= i
                
                self.retry_= 0
                
                if not eng== None: 
                    
                    eng.click()
                    
                    time.sleep(self.waiting_time_)
                    
                    return True
                
                else: 
                    return False
                
            except:
                
                time.sleep(self.waiting_time_)
                
                self.retry_+= 1
                
                if self.retry_== 100: return False
                
                continue
                        
            
    def number_of_review(self):
        
        num= self.driver.find_elements_by_class_name(self.num_reviews_class_name_)[self.language_idx_].text
        num= re.sub(re.compile('[()]'), '', num).replace(' ', '')
        
        return int(num)
        

    def next_page(self):
        
        ui_element_= self.driver.find_element_by_class_name(self.page_list_class_name_)
        ui_list_= ui_element_.find_elements_by_class_name(self.ui_class_name_)
        
        while True:
            
            try:
                
                for ui_ in ui_list_:
                    
                    if ui_.text== 'Next': ui_.click()
                    
            except:
                
                self.retry_+= 1
                if self.retry_%10== 0: self.refresh()
                
                time.sleep(self.waiting_time_)
                
                continue
            
            self.retry_= 0
            
            break
        
        
    def page_move(self):
        
        while True:
            
            try:
        
                _, y_loc_= self.driver.find_element_by_class_name(self.location_class_name_).location.values()
                self.driver.execute_script('window.scrollTo(0, %s);'%(y_loc_- 500))
                
            except:
                
                time.sleep(self.waiting_time_)
                
                self.retry_+= 1
                if self.retry_== 100: 
                    self.refresh()
                    self.page_move()
                
                continue
            
            self.retry_= 0
            
            break
        
        
    def read_more(self):
        
        self.page_move()
        
        more_list_= self.driver.find_elements_by_class_name(self.read_more_class_name_)
        
        if len(more_list_)!= 0:
            more_list_[0].click()
    
    
    def get_inpage_review(self):
        
        while True:
            try:
                self.read_more()
            except:
                time.sleep(self.waiting_time_)
                continue
            break
        
        reviewlist_= self.driver.find_elements_by_class_name(self.reviewlist_class_name_)
        
        self.hotel_name_= self.driver.find_element_by_css_selector(self.hotel_name_selector_).text.replace(' ', '_')
        
        try:
            self.hotel_star_= int(self.driver.find_element_by_class_name(self.star_class_name_).get_attribute('class').split()[1][5:])/10
        except:
            self.hotel_star_= 0
            
        try:
            self.hotel_price_= self.driver.find_element_by_class_name(self.price_class_name_).text
            self.hotel_price_= ''.join([n for n in re.findall('\d+', self.hotel_price_)])
        except:
            self.hotel_price_= 0
        
        
        time.sleep(self.waiting_time_)

        while True:
            
            try:
                hotel_name_list= []
                hotel_star_list= []
                hotel_price_list= []
                writer_list= []
                date_list= []
                rating_list= []
                review_list= []
                stay_list= []
        
                for review_ in reviewlist_:
                        
                    writer_, date_= self.get_writer_info(review_)
                    
                    hotel_name_list.append(self.hotel_name_)
                    hotel_star_list.append(self.hotel_star_)
                    hotel_price_list.append(self.hotel_price_)
                    writer_list.append(writer_)
                    date_list.append(date_)
                    rating_list.append(self.get_rating_info(review_))
                    review_list.append(review_.find_element_by_class_name(self.review_class_name_).text)
                    try:
                        stay_list.append(review_.find_element_by_class_name(self.stay_class_name_).text[14:])
                    except: 
                        stay_list.append('January 1900')
                        
                self.hotel_name_list_.extend(hotel_name_list)
                self.hotel_star_list_.extend(hotel_star_list)
                self.hotel_price_list_.extend(hotel_price_list)
                self.writer_list_.extend(writer_list)
                self.date_list_.extend(date_list)
                self.rating_list_.extend(rating_list)
                self.review_list_.extend(review_list)
                self.stay_list_.extend(stay_list)
                    
            except:
                
                self.retry_+= 1
                if self.retry_%10== 0: 
                    self.refresh()
                    self.page_move()
                    self.read_more()
                    
                time.sleep(self.waiting_time_)
            
                continue
            
            self.retry_= 0
            
            break
            
            
    def get_writer_info(self, review_):
        
        info_= review_.find_element_by_class_name(self.writer_class_name_).text
        
        writer_= info_[:info_.find(' wrote')]
        date_info_= info_.split()[-2:]
        
        if date_info_[0] not in self.month_list_: date_info_[0]= self.current_month_
        if not bool(re.search('\d{4}', date_info_[1])): date_info_[1]= self.current_year_
        
        date_= ' '.join([str(d_) for d_ in date_info_])
        
        return writer_, date_
    
    
    def get_rating_info(self, review_):
        
        rating= int(review_.find_element_by_class_name(self.rating_class_name_).get_attribute('class')[-2:])
        
        return rating/ 10
                
            
    def get_df(self):
        
        df= {}
        df['hotel']= self.hotel_name_list_
        df['star']= self.hotel_star_list_
        df['price']= self.hotel_price_list_
        df['writer']= self.writer_list_
        df['date']= self.date_list_
        df['rating']= self.rating_list_
        df['review']= self.review_list_
        df['stay']= self.stay_list_
        
        df= pd.DataFrame(df, columns= ['hotel', 'star', 'price', 'writer', \
                                       'date', 'rating', 'review', 'stay'])
        
        df.to_csv('../tripadvisor_hotels/%s.csv'%self.hotel_name_, sep= ',', index= False)
        
        self.save= True
    
        return df
    
    
    def refresh(self):
        
        if self.current_url_[-8:]!= '#REVIEWS': 
            self.hotel_url_= self.driver.current_url+ '#REVIEWS'
            
        self.driver.get(self.hotel_url_)
        time.sleep(self.waiting_time_* 5)
                
            
    def execute(self):
        
        while True:
            
            self.current_url_= self.driver.current_url
            
            if self.current_url_[-8:]!= '#REVIEWS': 
                self.hotel_url_+= '#REVIEWS'
                self.refresh()
                time.sleep(self.waiting_time_* 5)
                continue
            
            if not self.select_eng(): break
            if self.number_of_review()== 0: break
            
            self.get_inpage_review()
            
            if self.number_of_review()<= 5:
                
                self.get_df()
                break
                
            self.endpage_= self.get_endpage_info()
            
            for _ in range(self.endpage_- 1):
                
                self.next_page()
                self.get_inpage_review()
            
            self.get_df()
            
            break
        
        if not self.save:
            print(self.hotel_url_)
            
        self.driver.close()
            
    
if __name__=='__main__':
    
    url_crawler= hotel_url_crawler(driver_directory= '../chromedriver.exe',
                                   list_url= 'https://www.tripadvisor.co.za/Hotels-g294197-Seoul-Hotels.html')
    url_crawler.execute()
    url_list= url_crawler.url_list_
    
    
    main_crawler= review_crawler(driver_directory= '../chromedriver.exe',
                                 hotel_url= 'https://www.tripadvisor.co.za/Hotel_Review-g294197-d3291689-Reviews-Stylish_M_Hotel-Seoul.html',
                                 current_month= 'Nov',
                                 current_year= '2019')
    main_crawler.execute()
    