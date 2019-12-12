# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 00:02:56 2019

@author: hongj
"""

from tripadvisor_hotels import hotel_review_crawler as hrc
import multiprocessing as mp
import pandas as pd

def main(url, driver_directory):
    
    driver_directory= driver_directory
    current_month= 'Nov'
    current_year= '2019'

    crawler= hrc.review_crawler(driver_directory= driver_directory,
                                hotel_url= url,
                                current_month= current_month,
                                current_year= current_year)
    
    crawler.execute()
    
    
if __name__== '__main__':
    
    driver_directory= '../chromedriver.exe'

#    url_crawler= hrc.hotel_url_crawler(driver_directory= '../chromedriver.exe',
#                                       list_url= 'https://www.tripadvisor.co.za/Hotels-g297884-Busan-Hotels.html')
#    url_crawler.execute()
#    url_list= url_crawler.url_list_
#    
#    url_list= pd.DataFrame(url_list)
#    url_list.to_csv('../busan_list.csv', index= False)
    
    url_list= pd.Series(pd.read_csv('../busan_list.csv')['0'])
    
    print('-'*30)
    print('The number of url is %s.'%len(url_list))
    print('-'*30)
        
#    for i, url in enumerate(url_list):
#        
#        print(i)
#        main(url, driver_directory)
        

    url_list= [(url, driver_directory) for url in url_list]

    mp.freeze_support()
    with mp.Pool(processes= 8) as pool:
        pool.starmap(main, url_list)